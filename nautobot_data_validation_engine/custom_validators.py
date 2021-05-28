"""
This is the meat of this plugin.

Here we dynamically generate a PluginCustomValidator class
for each model currently registered in the extras_features
query registry 'custom_validators'.

A common clean method for all these classes looks for any
validation rules that have been defined for the given model.
"""
import re
from django.db.models.query_utils import Q

from nautobot.extras.plugins import PluginCustomValidator
from nautobot.extras.registry import registry

from nautobot_data_validation_engine.models import MinMaxValidationRule, RegularExpressionValidationRule


class BaseValidator(PluginCustomValidator):
    """
    Base PluginCustomValidator class that implements the core logic for enforcing validation rules defined in this plugin.
    """

    model = None

    def clean(self):
        """
        The clean method executes the actual rule enforcement logic for each model.
        """
        obj = self.context["object"]

        # Regex rules
        for rule in RegularExpressionValidationRule.objects.get_for_model(self.model):
            field_value = getattr(obj, rule.field)
            if field_value is None:
                # Coerce to a string for regex validation
                field_value = ""
            if not re.match(rule.regular_expression, field_value):
                self.validation_error(
                    {rule.field: rule.error_message or f"Value does not conform to regex: {rule.regular_expression}"}
                )

        # Min/Max rules
        for rule in MinMaxValidationRule.objects.get_for_model(self.model):
            field_value = getattr(obj, rule.field)

            if field_value is None:
                self.validation_error(
                    {
                        rule.field: rule.error_message
                        or f"Value does not conform to mix/max validation: min {rule.min}, max {rule.max}"
                    }
                )

            elif not isinstance(field_value, (int, float)):
                self.validation_error(
                    {
                        rule.field: f"Unable to validate against min/max rule {rule} because the field value is not numeric."
                    }
                )

            elif rule.min is not None and field_value is not None and field_value < rule.min:
                self.validation_error(
                    {rule.field: rule.error_message or f"Value is less than minimum value: {rule.min}"}
                )

            elif rule.max is not None and field_value is not None and field_value > rule.max:
                self.validation_error(
                    {rule.field: rule.error_message or f"Value is more than maximum value: {rule.max}"}
                )


class CustomValidatorIterator:
    """
    Iterator that generates PluginCustomValidator classes for each model registered in the extras feature query registry 'custom_validators'.
    """

    def __iter__(self):
        """
        Return a generator of PluginCustomValidator classes for each registered model.
        """
        for app_label, models in registry["model_features"]["custom_validators"].items():
            for model in models:
                yield type(
                    f"{app_label.capitalize()}{model.capitalize()}CustomValidator",
                    (BaseValidator,),
                    {"model": f"{app_label}.{model}"},
                )


custom_validators = CustomValidatorIterator()
