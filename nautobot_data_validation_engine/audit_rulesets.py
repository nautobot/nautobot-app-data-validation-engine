"""Validation class."""

import inspect
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.core.exceptions import ValidationError

from nautobot.extras.plugins import CustomValidator
from nautobot.extras.registry import registry

from nautobot_data_validation_engine.models import AuditResult


def is_audit_rule_set(obj):
    return inspect.isclass(obj) and issubclass(obj, AuditRuleset)


def get_audit_rule_sets_map():
    audit_rulesets = {}
    for validators in registry["plugin_custom_validators"].value():
        for validator in validators:
            if is_audit_rule_set(validator):
                audit_rulesets.setdefault(validator.model, [])
                audit_rulesets[validator.model].append(validator)

    return audit_rulesets


def get_audit_rule_sets():
    validators = []
    for rule_sets in get_audit_rule_sets_map().values():
        validators.extend(rule_sets)
    return validators


class AuditError(ValidationError):
    """An audit error is raised only when an object fails an audit."""


class AuditRuleset(CustomValidator):
    """Class to handle a set of validation functions."""

    model: str
    result_date: timezone
    valid = True
    enforce = False

    def __init__(self, obj):
        super().__init__(obj)
        self.result_date = timezone.now()

    def clean(self):
        try:
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
            if self.enforce:
                raise ex

    def audit_error(self, message):
        raise AuditError(message)

    def audit_result(self, message, attribute=None, valid=True):
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
                "validated_attribute_value": attribute_value,
                "message": message,
                "valid": valid,
            },
        )
        result.validated_save()
