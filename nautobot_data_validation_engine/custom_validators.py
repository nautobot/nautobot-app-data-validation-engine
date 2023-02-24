"""
This is the meat of this plugin.

Here we dynamically generate a PluginCustomValidator class
for each model currently registered in the extras_features
query registry 'custom_validators'.

A common clean method for all these classes looks for any
validation rules that have been defined for the given model.
"""
import re
import logging

from django.template.defaultfilters import pluralize

from nautobot.extras.plugins import PluginCustomValidator
from nautobot.extras.registry import registry
from nautobot.utilities.utils import render_jinja2

from nautobot_data_validation_engine.models import (
    MinMaxValidationRule,
    RegularExpressionValidationRule,
    RequiredValidationRule,
    UniqueValidationRule,
    validate_regex,
)

LOGGER = logging.getLogger(__name__)


def is_empty_value(value):
    return value is None or value == "" or value == [] or value == {}


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

            if rule.context_processing:
                # Render the regular_expression as a jinja2 string and ensure it is valid
                try:
                    regular_expression = render_jinja2(rule.regular_expression, self.context)
                    validate_regex(regular_expression)
                except Exception:
                    self.validation_error(
                        {
                            rule.field: f"There was an error rendering the regular expression in the data validation rule '{rule}'. "
                            "Either fix the validation rule or disable it in order to save this data."
                        }
                    )
                    LOGGER.exception(
                        f"There was an error rendering the regular expression in the data validation rule '{rule}' and a ValidationError was raised!"
                    )

            else:
                regular_expression = rule.regular_expression

            if not re.match(regular_expression, field_value):
                self.validation_error(
                    {rule.field: rule.error_message or f"Value does not conform to regex: {regular_expression}"}
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

        # Required rules
        for rule in RequiredValidationRule.objects.get_for_model(self.model):
            field_value = getattr(obj, rule.field)
            if is_empty_value(field_value):
                self.validation_error({rule.field: rule.error_message or "This field cannot be blank."})

        # Unique rules
        for rule in UniqueValidationRule.objects.get_for_model(self.model):
            field_value = getattr(obj, rule.field)
            if (
                not is_empty_value(field_value)
                and obj.__class__._default_manager.filter(**{rule.field: field_value}).count() >= rule.max_instances
            ):
                self.validation_error(
                    {
                        rule.field: rule.error_message
                        or f"There can only be {rule.max_instances} instance{pluralize(rule.max_instances)} with this value."
                    }
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
