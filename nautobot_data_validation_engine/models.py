"""Django models."""

import re

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.validators import MinValueValidator, ValidationError
from django.db import models
from django.shortcuts import reverse

from nautobot.core.models.generics import PrimaryModel
from nautobot.extras.utils import FeatureQuery, extras_features
from nautobot.core.models.querysets import RestrictedQuerySet


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
    """Adds a helper method for getting all active instances for a given content type."""

    def get_for_model(self, content_type):
        """Given a content type string (<app_label>.<model>), return all instances that are enabled for that model."""
        app_label, model = content_type.split(".")

        return self.filter(enabled=True, content_type__app_label=app_label, content_type__model=model)


class ValidationRule(PrimaryModel):
    """Base model for all validation engine rule models."""

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
        """Model metadata for all validation engine rule models."""

        abstract = True

    def __str__(self):
        """Return a sane string representation of the instance."""
        return self.name


@extras_features(
    "custom_fields",
    "custom_links",
    "export_templates",
    "graphql",
    "relationships",
    "statuses",
    "webhooks",
)
class RegularExpressionValidationRule(ValidationRule):
    """A type of validation rule that applies a regular expression to a given model field."""

    field = models.CharField(
        max_length=50,
    )
    regular_expression = models.TextField()
    context_processing = models.BooleanField(
        default=False,
        help_text="When enabled, the regular expression value is first processed as a Jinja2 template with access to the context of the data being validated in a variable named <code>object</code>.",
    )

    csv_headers = ["name", "slug", "enabled", "content_type", "field", "regular_expression", "error_message"]
    clone_fields = ["enabled", "content_type", "regular_expression", "error_message"]

    class Meta:
        """Model metadata for the RegularExpressionValidationRule model."""

        ordering = ("name",)
        unique_together = [["content_type", "field"]]

    def get_absolute_url(self):
        """Absolute url for the instance."""
        return reverse("plugins:nautobot_data_validation_engine:regularexpressionvalidationrule", args=[self.slug])

    def to_csv(self):
        """Return tuple representing the instance, which this used for CSV export."""
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
        """Ensure field is valid for the model and has not been blacklisted."""
        # Only validate the regular_expression if context processing is disabled
        if not self.context_processing:
            validate_regex(self.regular_expression)

        # Check that field exists on model
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


@extras_features(
    "custom_fields",
    "custom_links",
    "export_templates",
    "graphql",
    "relationships",
    "statuses",
    "webhooks",
)
class MinMaxValidationRule(ValidationRule):
    """A type of validation rule that applies min/max constraints to a given numeric model field."""

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
        """Model metadata for the MinMaxValidationRule model."""

        ordering = ("name",)
        unique_together = [["content_type", "field"]]

    def get_absolute_url(self):
        """Absolute url for the instance."""
        return reverse("plugins:nautobot_data_validation_engine:minmaxvalidationrule", args=[self.slug])

    def to_csv(self):
        """Return tuple representing the instance, which this used for CSV export."""
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
        """Ensure field is valid for the model and has not been blacklisted."""
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


@extras_features(
    "custom_fields",
    "custom_links",
    "export_templates",
    "graphql",
    "relationships",
    "statuses",
    "webhooks",
)
class RequiredValidationRule(ValidationRule):
    """A type of validation rule that applies a required constraint to a given model field."""

    field = models.CharField(
        max_length=50,
    )

    csv_headers = ["name", "slug", "enabled", "content_type", "field", "error_message"]
    clone_fields = ["enabled", "content_type", "error_message"]

    class Meta:
        """Model metadata for the RequiredValidationRule model."""

        ordering = ("name",)
        unique_together = [["content_type", "field"]]

    def get_absolute_url(self):
        """Absolute url for the instance."""
        return reverse("plugins:nautobot_data_validation_engine:requiredvalidationrule", args=[self.slug])

    def to_csv(self):
        """Return tuple representing the instance, which this used for CSV export."""
        return (
            self.name,
            self.slug,
            self.enabled,
            f"{self.content_type.app_label}.{self.content_type.model}",
            self.field,
            self.error_message,
        )

    def clean(self):
        """Ensure field is valid for the model and has not been blacklisted."""
        if self.field not in [f.name for f in self.content_type.model_class()._meta.get_fields()]:
            raise ValidationError(
                {
                    "field": f"Not a valid field for content type {self.content_type.app_label}.{self.content_type.model}."
                }
            )

        blacklisted_field_types = (
            models.AutoField,
            models.Manager,
            models.fields.related.RelatedField,
            models.ManyToManyField,
        )

        model_field = self.content_type.model_class()._meta.get_field(self.field)

        if self.field.startswith("_") or not model_field.editable or isinstance(model_field, blacklisted_field_types):
            raise ValidationError({"field": "This field's type does not support required validation."})

        # Generally, only Field(null=True) is considered except for the case of Field(null=False, blank=True)
        # which is commonly seen on CharFields and results in a default of empty string which is unacceptable
        # if the field is to be marked as required.
        if model_field.null is False and not (model_field.null is False and model_field.blank is True):
            raise ValidationError({"field": "This field is already required by default."})


@extras_features(
    "custom_fields",
    "custom_links",
    "export_templates",
    "graphql",
    "relationships",
    "statuses",
    "webhooks",
)
class UniqueValidationRule(ValidationRule):
    """
    A type of validation rule that applies a unique constraint to a given model field.

    Optionally specify the max number of similar values for the field accross all model instances. Default of 1.
    """

    field = models.CharField(
        max_length=50,
    )
    max_instances = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    csv_headers = ["name", "slug", "enabled", "content_type", "field", "max_instances", "error_message"]
    clone_fields = ["enabled", "content_type", "max_instances", "error_message"]

    class Meta:
        """Model metadata for the UniqueValidationRule model."""

        ordering = ("name",)
        unique_together = [["content_type", "field"]]

    def get_absolute_url(self):
        """Absolute url for the instance."""
        return reverse("plugins:nautobot_data_validation_engine:uniquevalidationrule", args=[self.slug])

    def to_csv(self):
        """Return tuple representing the instance, which this used for CSV export."""
        return (
            self.name,
            self.slug,
            self.enabled,
            f"{self.content_type.app_label}.{self.content_type.model}",
            self.field,
            self.max_instances,
            self.error_message,
        )

    def clean(self):
        """Ensure field is valid for the model and has not been blacklisted."""
        if self.field not in [f.name for f in self.content_type.model_class()._meta.get_fields()]:
            raise ValidationError(
                {
                    "field": f"Not a valid field for content type {self.content_type.app_label}.{self.content_type.model}."
                }
            )

        blacklisted_field_types = (
            models.Manager,
            models.fields.related.RelatedField,
            models.ManyToManyField,
        )

        model_field = self.content_type.model_class()._meta.get_field(self.field)

        if self.field.startswith("_") or not model_field.editable or isinstance(model_field, blacklisted_field_types):
            raise ValidationError({"field": "This field's type does not support uniqueness validation."})

        if getattr(model_field, "unique", False):
            raise ValidationError({"field": "This field is already unique by default."})


class DataCompliance(PrimaryModel):
    """Model to represent the results of an audit method."""

    compliance_class_name = models.CharField(max_length=100, blank=False, null=False)
    last_validation_date = models.DateTimeField(blank=False, null=False, auto_now=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT, blank=False, null=False)
    object_id = models.CharField(max_length=200, blank=False, null=False)
    validated_object = GenericForeignKey("content_type", "object_id")
    validated_object_str = models.CharField(max_length=200, blank=True, null=True)
    validated_attribute = models.CharField(max_length=100, blank=True, null=True)
    validated_attribute_value = models.CharField(max_length=200, blank=True, null=True)
    valid = models.BooleanField(blank=False, null=False)
    message = models.TextField(blank=True, null=True)

    csv_headers = [
        "compliance_class_name",
        "last_validation_date",
        "validated_object",
        "validated_attribute",
        "validated_attribute_value",
        "valid",
        "message",
    ]

    class Meta:
        """Meta class for Audit model."""

        verbose_name_plural = "Data Compliance"

        unique_together = (
            "compliance_class_name",
            "content_type",
            "object_id",
            "validated_attribute",
        )

    def to_csv(self):
        """Return a tuple of data that should be exported to CSV."""
        return (
            self.compliance_class_name,
            self.last_validation_date,
            self.validated_object,
            self.validated_attribute,
            self.validated_attribute_value,
            self.valid,
            self.message,
        )

    def __str__(self):
        """Return a string representation of this DataCompliance object."""
        return f"{self.compliance_class_name}: {self.validated_attribute} compliance for {self.validated_object}"

    def get_absolute_url(self):
        """Return the absolute URL to this Audit object."""
        return reverse("plugins:nautobot_data_validation_engine:datacompliance", args=[self.pk])
