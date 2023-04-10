from nautobot_data_validation_engine.models import ValidationResult
from django.apps import apps as global_apps
from django.utils import timezone
import inspect
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError


class ValidationSet:
    model: str
    result_date: timezone

    def __init__(self):
        self.result_date = timezone.now()
        self.job_result = None

    def __find_calling_method_name(self):
        stack = inspect.stack()
        for frame in stack:
            if frame.function.startswith("validate_"):
                return frame.function
        raise Exception("Unable to find calling method that starts with 'validate_'.")

    def __generate_result(
        self,
        valid,
        validated_object,
        attribute=None,
        validated_attribute_value=None,
        expected_attribute_value=None,
        message=None,
    ):
        class_name = type(self).__name__
        method_name = self.__find_calling_method_name()
        content_type = ContentType.objects.get_for_model(validated_object)
        result = ValidationResult.objects.filter(
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
            result = ValidationResult(
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
        return self.__generate_result(True, obj, **kwargs)

    def fail(self, obj, **kwargs):
        return self.__generate_result(False, obj, **kwargs)

    def get_queryset(self):
        model = global_apps.get_model(self.model)
        return model.objects.all()

    def _validate_all(self):
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

    def validate(self, job_result):
        self.job_result = job_result
        validation_functions = [
            function
            for name, function in inspect.getmembers(self, predicate=inspect.ismethod)
            if name.startswith("validate_")
        ]
        for obj in self.get_queryset():
            for function in validation_functions:
                function(obj)


class ValidationSetAll(ValidationSet):
    model = "faker"

    def validate(self, job_result):
        """."""
        self.job_result = job_result
        self.validate_full_clean()

    def validate_full_clean(self):
        self._validate_all()


validations = [ValidationSetAll]
