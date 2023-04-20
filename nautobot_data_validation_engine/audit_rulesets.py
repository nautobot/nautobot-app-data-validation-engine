"""Validation class."""

import inspect
from typing import Optional
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError

from nautobot.extras.plugins import CustomValidator
from nautobot.extras.registry import registry

from nautobot_data_validation_engine.models import AuditResult


def is_audit_rule_set(obj):
    """Check to see if object is an AuditRuleset class instance."""
    return inspect.isclass(obj) and issubclass(obj, AuditRuleset)


def get_audit_rule_sets_map():
    """Generate a dictionary of audit rulesets associated to their models."""
    audit_rulesets = {}
    for validators in registry["plugin_custom_validators"].values():
        for validator in validators:
            if is_audit_rule_set(validator):
                audit_rulesets.setdefault(validator.model, [])
                audit_rulesets[validator.model].append(validator)

    return audit_rulesets


def get_audit_rule_sets():
    """Generate a list of Audit Ruleset classes that exist from the registry."""
    validators = []
    for rule_sets in get_audit_rule_sets_map().values():
        validators.extend(rule_sets)
    return validators


class AuditError(ValidationError):
    """An audit error is raised only when an object fails an audit."""


class AuditRuleset(CustomValidator):
    """Class to handle a set of validation functions."""

    class_name: Optional[str] = None
    method_names: dict = {}
    model: str
    result_date: timezone
    valid = True
    enforce = False

    def __init__(self, obj):
        """Initialize an AuditRuleset object."""
        super().__init__(obj)
        self.result_date = timezone.now()

    def audit(self):
        """Not implemented.  Should raise an AuditError if an attribute is found to be invalid."""
        raise NotImplementedError

    def mark_all_existing_as_valid(self):
        """Mark all existing fields (any that were previously created) as valid=True."""
        instance = self.context["object"]
        attributes = (
            AuditResult.objects.filter(
                audit_class_name=self.__class__.__name__,
                content_type=ContentType.objects.get_for_model(instance),
                object_id=instance.id,
            )
            .exclude(validated_attribute="all")
            .values_list("validated_attribute", flat=True)
        )
        for attribute in attributes:
            self.audit_result(message=f"{attribute} is valid.", attribute=attribute)

    def clean(self):
        """Override the clean method to run the audit function."""
        try:
            self.mark_all_existing_as_valid()
            self.audit()
            self.audit_result(message=f"{self.context['object']} is valid")
        except AuditError as ex:
            try:
                for attribute, messages in ex.message_dict.items():
                    for message in messages:
                        self.audit_result(message=message, attribute=attribute, valid=False)
            except AttributeError:
                for message in ex.messages:
                    self.audit_result(message=message, valid=False)
            finally:
                self.audit_result(message=f"{self.context['object']} is not valid", valid=False)
            if self.enforce:
                raise ex

    @staticmethod
    def audit_error(message):
        """Raise an Audit Error with the given message."""
        raise AuditError(message)

    def audit_result(self, message, attribute=None, valid=True):
        """Generate an Audit Result object based on the given parameters."""
        instance = self.context["object"]
        attribute_value = None
        if attribute:
            attribute_value = getattr(instance, attribute)
        else:
            attribute = "all"
        result, _ = AuditResult.objects.update_or_create(
            audit_class_name=self.__class__.__name__,
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.id,
            validated_attribute=attribute,
            defaults={
                "last_validation_date": self.result_date,
                "validated_attribute_value": str(attribute_value) if attribute_value else None,
                "message": message,
                "valid": valid,
            },
        )
        result.validated_save()
