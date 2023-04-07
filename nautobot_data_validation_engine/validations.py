from nautobot_data_validation_engine.models import ValidationResult
from django.apps import apps as global_apps
from datetime import datetime
import inspect
from django.contrib.contenttypes.models import ContentType


class ValidationSet:
    model: str
    result_date: datetime

    def __init__(self):
        self.result_date = datetime.now()

    def __find_calling_method_name(self):
        stack = inspect.stack()
        for frame in stack:
            if frame.function.startswith("validate_"):
                return frame.function
        raise Exception("Unable to find calling method that starts with 'validate_'.")

    def __generate_result(self, valid, obj, attribute=None, current_value=None, expected_value=None, message=None):
        class_name = type(self).__name__
        method_name = self.__find_calling_method_name()
        content_type = ContentType.objects.get_for_model(obj)
        result = ValidationResult.objects.filter(
            class_name=class_name,
            method_name=method_name,
            content_type=content_type,
            object_id=obj.id,
            validated_attribute=attribute,
        ).first()
        if result:
            result.last_validation_date = datetime.now()
            result.valid = valid
            result.message = message
        else:
            result = ValidationResult(
                class_name=class_name,
                method_name=method_name,
                last_validation_date=datetime.now(),
                validated_object=obj,
                validated_attribute=attribute if attribute else None,
                validated_attribute_value=str(current_value) if current_value else None,
                expected_attribute_value=str(expected_value) if expected_value else None,
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

    def validate(self):
        validation_functions = [
            function
            for name, function in inspect.getmembers(self, predicate=inspect.ismethod)
            if name.startswith("validate_")
        ]
        for obj in self.get_queryset():
            for function in validation_functions:
                function(obj)
