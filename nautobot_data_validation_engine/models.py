"""
Django models.
"""
import re

from django.contrib.contenttypes.models import ContentType
from django.core.validators import ValidationError
from django.db import models
from django.db.models.query_utils import Q
from django.shortcuts import reverse

from nautobot.extras.models import ChangeLoggedModel
from nautobot.extras.utils import FeatureQuery
from nautobot.utilities.querysets import RestrictedQuerySet

from nautobot.core.models import BaseModel


def validate_regex(value):
    """
    Checks that the value is a valid regular expression.

    Don't confuse this with RegexValidator, which *uses* a regex to validate a value.
    """
    try:
        re.compile(value)
    except re.error:
        raise ValidationError(f"{value} is not a valid regular expression.")


class ValidationRuleManager(RestrictedQuerySet):
    """
    Adds a helper method for getting all active instances for a given content type.
    """

    def get_for_model(self, content_type):
        """
        Given a content type string (<app_label>.<model>), return all instances that are enabled for that model.
        """
        app_label, model = content_type.split(".")

        return self.filter(enabled=True, content_type__app_label=app_label, content_type__model=model)


class ValidationRule(BaseModel, ChangeLoggedModel):
    """
    Base model for all validation engine rule models
    """

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    content_type = models.ForeignKey(
        to=ContentType, on_delete=models.CASCADE, limit_choices_to=FeatureQuery("custom_validators")
    )
    enabled = models.BooleanField(default=True)
    error_message = models.CharField(
        max_length=255, null=True, blank=True, help_text="Optional error message to display when validation fails."
    )

    objects = ValidationRuleManager.as_manager()

    class Meta:
        abstract = True

    def __str__(self):
        """
        Return a sane string representation of the instance.
        """
        return self.name


class RegularExpressionValidationRule(ValidationRule):
    """
    A type of validation rule that applies a regular expression to a given model field.
    """

    field = models.CharField(
        max_length=50,
    )
    regular_expression = models.TextField(validators=[validate_regex])

    csv_headers = ["name", "slug", "enabled", "content_type", "field", "regular_expression", "error_message"]
    clone_fields = ["enabled", "content_type", "regular_expression", "error_message"]

    class Meta:
        ordering = ("name",)
        unique_together = [["content_type", "field"]]

    def get_absolute_url(self):
        """
        Absolute url for the instance.
        """
        return reverse("plugins:nautobot_data_validation_engine:regularexpressionvalidationrule", args=[self.slug])

    def to_csv(self):
        """
        Return tuple representing the instance, which this used for CSV export.
        """
        return (
            self.name,
            self.slug,
            self.enabled,
            f"{self.content_type.app_label}.{self.content_type.model}",
            self.field,
            self.regular_expression,
            self.error_message,
        )

    def clean(self):
        """
        Ensure field is valid for the model and has not been blacklisted.
        """
        if self.field not in [f.name for f in self.content_type.model_class()._meta.get_fields()]:
            raise ValidationError(
                {
                    "field": f"Not a valid field for content type {self.content_type.app_label}.{self.content_type.model}."
                }
            )

        blacklisted_field_types = (
            models.AutoField,
            models.BigAutoField,
            models.BooleanField,
            models.FileField,
            models.FilePathField,
            models.ForeignKey,
            models.ImageField,
            models.JSONField,
            models.Manager,
            models.ManyToManyField,
            models.NullBooleanField,
            models.OneToOneField,
            models.fields.related.RelatedField,
            models.SmallAutoField,
            models.UUIDField,
        )

        model_field = self.content_type.model_class()._meta.get_field(self.field)

        if self.field.startswith("_") or not model_field.editable or isinstance(model_field, blacklisted_field_types):
            raise ValidationError({"field": "This field's type does not support regular expression validation."})


class MinMaxValidationRule(ValidationRule):
    """
    A type of validation rule that applies min/max constraints to a given numeric model field.
    """

    field = models.CharField(
        max_length=50,
    )
    min = models.FloatField(
        null=True, blank=True, help_text="When set, apply a minimum value contraint to the value of the model field."
    )
    max = models.FloatField(
        null=True, blank=True, help_text="When set, apply a maximum value contraint to the value of the model field."
    )

    csv_headers = ["name", "slug", "enabled", "content_type", "field", "min", "max", "error_message"]
    clone_fields = ["enabled", "content_type", "min", "max", "error_message"]

    class Meta:
        ordering = ("name",)
        unique_together = [["content_type", "field"]]

    def get_absolute_url(self):
        """
        Absolute url for the instance.
        """
        return reverse("plugins:nautobot_data_validation_engine:minmaxvalidationrule", args=[self.slug])

    def to_csv(self):
        """
        Return tuple representing the instance, which this used for CSV export.
        """
        return (
            self.name,
            self.slug,
            self.enabled,
            f"{self.content_type.app_label}.{self.content_type.model}",
            self.field,
            self.min,
            self.max,
            self.error_message,
        )

    def clean(self):
        """
        Ensure field is valid for the model and has not been blacklisted.
        """
        if self.field not in [f.name for f in self.content_type.model_class()._meta.get_fields()]:
            raise ValidationError(
                {
                    "field": f"Not a valid field for content type {self.content_type.app_label}.{self.content_type.model}."
                }
            )

        whitelisted_field_types = (
            models.DecimalField,
            models.FloatField,
            models.IntegerField,
        )

        blacklisted_field_types = (
            models.AutoField,
            models.BigAutoField,
        )

        model_field = self.content_type.model_class()._meta.get_field(self.field)

        if not isinstance(model_field, whitelisted_field_types) or (
            self.field.startswith("_") or not model_field.editable or isinstance(model_field, blacklisted_field_types)
        ):
            raise ValidationError({"field": "This field's type does not support min/max validation."})

        if self.min is None and self.max is None:
            raise ValidationError("At least a minimum or maximum value must be specified.")

        if self.min is not None and self.max is not None and self.min > self.max:
            raise ValidationError(
                {
                    "min": "Minimum value cannot be more than the maximum value.",
                    "max": "Maximum value cannot be less than the minimum value.",
                }
            )
