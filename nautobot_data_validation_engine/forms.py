"""Django forms."""

from django import forms
from django.contrib.contenttypes.models import ContentType

from nautobot.extras.utils import FeatureQuery
from nautobot.utilities.forms import (
    BootstrapMixin,
    BulkEditForm,
    BulkEditNullBooleanSelect,
    CSVContentTypeField,
    CSVMultipleContentTypeField,
    CSVModelForm,
    SlugField,
    StaticSelect2,
)
from nautobot.utilities.forms.constants import BOOLEAN_WITH_BLANK_CHOICES

from nautobot_data_validation_engine.models import (
    MinMaxValidationRule,
    RegularExpressionValidationRule,
    RequiredValidationRule,
    UniqueValidationRule,
    ValidationResult,
)


#
# RegularExpressionValidationRules
#


class RegularExpressionValidationRuleForm(BootstrapMixin, forms.ModelForm):
    """Base model form for the RegularExpressionValidationRule model."""

    slug = SlugField()
    content_type = forms.ModelChoiceField(
        queryset=ContentType.objects.filter(FeatureQuery("custom_validators").get_query()).order_by(
            "app_label", "model"
        ),
    )

    class Meta:
        """Form metadata for the RegularExpressionValidationRule model."""

        model = RegularExpressionValidationRule
        fields = [
            "name",
            "slug",
            "enabled",
            "content_type",
            "field",
            "regular_expression",
            "context_processing",
            "error_message",
        ]


class RegularExpressionValidationRuleCSVForm(CSVModelForm):
    """Base csv form for the RegularExpressionValidationRule model."""

    slug = SlugField()
    content_type = CSVContentTypeField(
        queryset=ContentType.objects.filter(FeatureQuery("custom_validators").get_query()),
        help_text="The object type to which this regular expression rule applies.",
    )

    class Meta:
        """CSV form metadata for the RegularExpressionValidationRule model."""

        model = RegularExpressionValidationRule
        fields = RegularExpressionValidationRule.csv_headers


class RegularExpressionValidationRuleBulkEditForm(BootstrapMixin, BulkEditForm):
    """Base bulk edit form for the RegularExpressionValidationRule model."""

    pk = forms.ModelMultipleChoiceField(
        queryset=RegularExpressionValidationRule.objects.all(), widget=forms.MultipleHiddenInput
    )
    enabled = forms.NullBooleanField(
        required=False,
        widget=BulkEditNullBooleanSelect(),
    )
    regular_expression = forms.CharField(required=False)
    error_message = forms.CharField(required=False)
    context_processing = forms.NullBooleanField(
        required=False,
        widget=BulkEditNullBooleanSelect(),
    )

    class Meta:
        """Bulk edit form metadata for the RegularExpressionValidationRule model."""

        nullable_fields = ["error_message"]


class RegularExpressionValidationRuleFilterForm(BootstrapMixin, forms.Form):
    """Base filter form for the RegularExpressionValidationRule model."""

    model = RegularExpressionValidationRule
    field_order = [
        "q",
        "name",
        "enabled",
        "content_type",
        "field",
        "regular_expression",
        "context_processing",
        "error_message",
    ]
    q = forms.CharField(required=False, label="Search")
    # "CSV" field is being used here because it is using the slug-form input for
    # content-types, which improves UX.
    content_type = CSVMultipleContentTypeField(
        queryset=ContentType.objects.filter(FeatureQuery("custom_validators").get_query()).order_by(
            "app_label", "model"
        ),
        required=False,
    )


#
# MinMaxValidationRules
#


class MinMaxValidationRuleForm(BootstrapMixin, forms.ModelForm):
    """Base model form for the MinMaxValidationRule model."""

    slug = SlugField()
    content_type = forms.ModelChoiceField(
        queryset=ContentType.objects.filter(FeatureQuery("custom_validators").get_query()).order_by(
            "app_label", "model"
        ),
    )

    class Meta:
        """Form metadata for the MinMaxValidationRule model."""

        model = MinMaxValidationRule
        fields = ["name", "slug", "enabled", "content_type", "field", "min", "max", "error_message"]


class MinMaxValidationRuleCSVForm(CSVModelForm):
    """Base csv form for the MinMaxValidationRule model."""

    slug = SlugField()
    content_type = CSVContentTypeField(
        queryset=ContentType.objects.filter(FeatureQuery("custom_validators").get_query()),
        help_text="The object type to which this min/max rule applies.",
    )

    class Meta:
        """CSV form metadata for the MinMaxValidationRule model."""

        model = MinMaxValidationRule
        fields = MinMaxValidationRule.csv_headers


class MinMaxValidationRuleBulkEditForm(BootstrapMixin, BulkEditForm):
    """Base bulk edit form for the MinMaxValidationRule model."""

    pk = forms.ModelMultipleChoiceField(queryset=MinMaxValidationRule.objects.all(), widget=forms.MultipleHiddenInput)
    enabled = forms.NullBooleanField(
        required=False,
        widget=BulkEditNullBooleanSelect(),
    )
    min = forms.IntegerField(required=False)
    max = forms.IntegerField(required=False)
    error_message = forms.CharField(required=False)

    class Meta:
        """Bulk edit form metadata for the MinMaxValidationRule model."""

        nullable_fields = ["error_message"]


class MinMaxValidationRuleFilterForm(BootstrapMixin, forms.Form):
    """Base filter form for the MinMaxValidationRule model."""

    model = MinMaxValidationRule
    field_order = ["q", "name", "enabled", "content_type", "field", "min", "max", "error_message"]
    q = forms.CharField(required=False, label="Search")
    # "CSV" field is being used here because it is using the slug-form input for
    # content-types, which improves UX.
    content_type = CSVMultipleContentTypeField(
        queryset=ContentType.objects.filter(FeatureQuery("custom_validators").get_query()).order_by(
            "app_label", "model"
        ),
        required=False,
    )
    min = forms.IntegerField(required=False)
    max = forms.IntegerField(required=False)


#
# RequiredValidationRules
#


class RequiredValidationRuleForm(BootstrapMixin, forms.ModelForm):
    """Base model form for the RequiredValidationRule model."""

    slug = SlugField()
    content_type = forms.ModelChoiceField(
        queryset=ContentType.objects.filter(FeatureQuery("custom_validators").get_query()).order_by(
            "app_label", "model"
        ),
    )

    class Meta:
        """Form metadata for the RequiredValidationRule model."""

        model = RequiredValidationRule
        fields = [
            "name",
            "slug",
            "enabled",
            "content_type",
            "field",
            "error_message",
        ]


class RequiredValidationRuleCSVForm(CSVModelForm):
    """Base csv form for the RequiredValidationRule model."""

    slug = SlugField()
    content_type = CSVContentTypeField(
        queryset=ContentType.objects.filter(FeatureQuery("custom_validators").get_query()),
        help_text="The object type to which this required field rule applies.",
    )

    class Meta:
        """CSV form metadata for the RequiredValidationRule model."""

        model = RequiredValidationRule
        fields = RequiredValidationRule.csv_headers


class RequiredValidationRuleBulkEditForm(BootstrapMixin, BulkEditForm):
    """Base bulk edit form for the RequiredValidationRule model."""

    pk = forms.ModelMultipleChoiceField(queryset=RequiredValidationRule.objects.all(), widget=forms.MultipleHiddenInput)
    enabled = forms.NullBooleanField(
        required=False,
        widget=BulkEditNullBooleanSelect(),
    )
    error_message = forms.CharField(required=False)

    class Meta:
        """Bulk edit form metadata for the RequiredValidationRule model."""

        nullable_fields = ["error_message"]


class RequiredValidationRuleFilterForm(BootstrapMixin, forms.Form):
    """Base filter form for the RequiredValidationRule model."""

    model = RequiredValidationRule
    field_order = [
        "q",
        "name",
        "enabled",
        "content_type",
        "field",
        "error_message",
    ]
    q = forms.CharField(required=False, label="Search")
    # "CSV" field is being used here because it is using the slug-form input for
    # content-types, which improves UX.
    content_type = CSVMultipleContentTypeField(
        queryset=ContentType.objects.filter(FeatureQuery("custom_validators").get_query()).order_by(
            "app_label", "model"
        ),
        required=False,
    )


#
# UniqueValidationRules
#


class UniqueValidationRuleForm(BootstrapMixin, forms.ModelForm):
    """Base model form for the UniqueValidationRule model."""

    slug = SlugField()
    content_type = forms.ModelChoiceField(
        queryset=ContentType.objects.filter(FeatureQuery("custom_validators").get_query()).order_by(
            "app_label", "model"
        ),
    )

    class Meta:
        """Form metadata for the UniqueValidationRule model."""

        model = UniqueValidationRule
        fields = [
            "name",
            "slug",
            "enabled",
            "content_type",
            "field",
            "max_instances",
            "error_message",
        ]


class UniqueValidationRuleCSVForm(CSVModelForm):
    """Base csv form for the UniqueValidationRule model."""

    slug = SlugField()
    content_type = CSVContentTypeField(
        queryset=ContentType.objects.filter(FeatureQuery("custom_validators").get_query()),
        help_text="The object type to which this unique field rule applies.",
    )

    class Meta:
        """CSV form metadata for the UniqueValidationRule model."""

        model = UniqueValidationRule
        fields = UniqueValidationRule.csv_headers


class UniqueValidationRuleBulkEditForm(BootstrapMixin, BulkEditForm):
    """Base bulk edit form for the UniqueValidationRule model."""

    pk = forms.ModelMultipleChoiceField(queryset=UniqueValidationRule.objects.all(), widget=forms.MultipleHiddenInput)
    enabled = forms.NullBooleanField(
        required=False,
        widget=BulkEditNullBooleanSelect(),
    )
    max_instances = forms.IntegerField(required=False)
    error_message = forms.CharField(required=False)

    class Meta:
        """Bulk edit form metadata for the UniqueValidationRule model."""

        nullable_fields = ["error_message"]


class UniqueValidationRuleFilterForm(BootstrapMixin, forms.Form):
    """Base filter form for the UniqueValidationRule model."""

    model = UniqueValidationRule
    field_order = [
        "q",
        "name",
        "enabled",
        "content_type",
        "field",
        "max_instances",
        "error_message",
    ]
    q = forms.CharField(required=False, label="Search")
    # "CSV" field is being used here because it is using the slug-form input for
    # content-types, which improves UX.
    content_type = CSVMultipleContentTypeField(
        queryset=ContentType.objects.filter(FeatureQuery("custom_validators").get_query()).order_by(
            "app_label", "model"
        ),
        required=False,
    )
    max_instances = forms.IntegerField(required=False)


class ValidationResultFilterForm(BootstrapMixin, forms.Form):
    """Form for ValidationResult instances."""

    model = ValidationResult
    class_name = forms.CharField(max_length=20, required=False)
    method_name = forms.CharField(max_length=20, required=False)
    validated_attribute = forms.CharField(max_length=20, required=False)
    valid = forms.NullBooleanField(required=False, widget=StaticSelect2(choices=BOOLEAN_WITH_BLANK_CHOICES))
    content_type = CSVContentTypeField(
        queryset=ContentType.objects.all().order_by("app_label", "model"), required=False
    )
    q = forms.CharField(required=False, label="Search")
