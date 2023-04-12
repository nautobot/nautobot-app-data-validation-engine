"""Validation class."""

import inspect
from django.apps import apps as global_apps
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from nautobot_data_validation_engine.models import AuditRule


class AuditRuleset:
    """Class to handle a set of validation functions."""

    model: str
    result_date: timezone

    def __init__(self):
        """Create a AuditRuleset object."""
        self.result_date = timezone.now()
        self.job_result = None

    def __find_calling_method_name(self):  # pylint: disable=R0201
        """Return the calling function that starts with 'audit_' by looking through the current stack."""
        stack = inspect.stack()
        for frame in stack:
            if frame.function.startswith("audit_"):
                return frame.function
        raise Exception("Unable to find calling method that starts with 'audit_'.")

    def __generate_result(  # pylint: disable=R0913
        self,
        valid,
        validated_object,
        attribute=None,
        validated_attribute_value=None,
        expected_attribute_value=None,
        message=None,
    ):
        """Report a audit rule."""
        class_name = type(self).__name__
        method_name = self.__find_calling_method_name()
        content_type = ContentType.objects.get_for_model(validated_object)
        result = AuditRule.objects.filter(
            class_name=class_name,
            method_name=method_name,
            content_type=content_type,
            object_id=validated_object.id,
            validated_attribute=attribute,
        ).first()
        if result:
            result.last_validation_date = self.result_date
            result.valid = valid
            result.message = message
        else:
            result = AuditRule(
                class_name=class_name,
                method_name=method_name,
                last_validation_date=self.result_date,
                validated_object=validated_object,
                validated_attribute=attribute if attribute else None,
                validated_attribute_value=str(validated_attribute_value) if validated_attribute_value else None,
                expected_attribute_value=str(expected_attribute_value) if expected_attribute_value else None,
                valid=valid,
                message=message,
            )
        result.save()

    def success(self, obj, **kwargs):
        """Report a successful audit check."""
        return self.__generate_result(True, obj, **kwargs)

    def fail(self, obj, **kwargs):
        """Report a failed audit check."""
        return self.__generate_result(False, obj, **kwargs)

    def get_queryset(self):
        """Return all objects of the given model in a queryset."""
        model = global_apps.get_model(self.model)
        return model.objects.all()

    def audit(self, job_result):
        """Run all functions from this class that start with 'audit_'."""
        self.job_result = job_result
        validation_functions = [
            function
            for name, function in inspect.getmembers(self, predicate=inspect.ismethod)
            if name.startswith("audit_")
        ]
        for obj in self.get_queryset():
            for function in validation_functions:
                function(obj)


class AuditRulesetAll(AuditRuleset):
    """AuditRuleset class for all content types."""

    model = "faker"

    def _validate_all(self):
        """Run full clean on all objects and report any objects that have ValidationErrors."""
        # Lambdas are used just to sort by attribute value.
        for app_config in sorted(list(global_apps.get_app_configs()), key=lambda x: x.label):
            for model in sorted(list(app_config.models.values()), key=lambda x: x._meta.model_name):
                model_name = f"{model._meta.app_label}.{model._meta.model_name}"
                # Must swap out for user_model
                if model_name == "auth.user":
                    model = get_user_model()
                # Skip models that aren't actually in the database
                if not model._meta.managed:
                    continue
                self.job_result.log_info(f" --> {type(self).__name__} is Validating Model: {model_name}")

                model.objects.all()
                for instance in model.objects.all().iterator():
                    try:
                        instance.full_clean()
                    except ValidationError as err:
                        for attribute, messages in err.message_dict.items():
                            self.fail(
                                instance,
                                attribute=attribute,
                                validated_attribute_value=getattr(instance, attribute),
                                message=" AND ".join(messages),
                            )

    def audit(self, job_result):
        """."""
        self.job_result = job_result
        self.audit_full_clean()

    def audit_full_clean(self):
        """Run full_clean on all objects and validate the results."""
        self._validate_all()


audit_rulesets = [AuditRulesetAll]
