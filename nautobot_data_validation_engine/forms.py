"""Django forms."""

from django import forms
from django.contrib.contenttypes.models import ContentType

from nautobot.core.forms import (
    BulkEditNullBooleanSelect,
    CSVMultipleContentTypeField,
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
    MultipleContentTypeField,
    StaticSelect2,
    TagFilterField,
)
from nautobot.core.forms.constants import BOOLEAN_WITH_BLANK_CHOICES
from nautobot.extras.forms import (
    NautobotBulkEditForm,
    NautobotFilterForm,
    NautobotModelForm,
    TagsBulkEditFormMixin,
)
from nautobot.extras.utils import FeatureQuery

from nautobot_data_validation_engine.models import (
    DataCompliance,
    MinMaxValidationRule,
    RegularExpressionValidationRule,
    RequiredValidationRule,
    UniqueValidationRule,
)


#
# RegularExpressionValidationRules
#


class RegularExpressionValidationRuleForm(NautobotModelForm):
    """Base model form for the RegularExpressionValidationRule model."""

    content_type = DynamicModelChoiceField(
        queryset=ContentType.objects.filter(FeatureQuery("custom_validators").get_query()).order_by(
            "app_label", "model"
        ),
    )

    class Meta:
        """Form metadata for the RegularExpressionValidationRule model."""

        model = RegularExpressionValidationRule
        fields = [
            "name",
            "enabled",
            "content_type",
            "field",
            "regular_expression",
            "context_processing",
            "error_message",
            "tags",
        ]


class RegularExpressionValidationRuleBulkEditForm(NautobotBulkEditForm, TagsBulkEditFormMixin):
    """Base bulk edit form for the RegularExpressionValidationRule model."""

    pk = DynamicModelMultipleChoiceField(
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

        fields = ["tags"]
        nullable_fields = ["error_message"]


class RegularExpressionValidationRuleFilterForm(NautobotFilterForm):
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
    tag = TagFilterField(model)


#
# MinMaxValidationRules
#


class MinMaxValidationRuleForm(NautobotModelForm):
    """Base model form for the MinMaxValidationRule model."""

    content_type = DynamicModelChoiceField(
        queryset=ContentType.objects.filter(FeatureQuery("custom_validators").get_query()).order_by(
            "app_label", "model"
        ),
    )

    class Meta:
        """Form metadata for the MinMaxValidationRule model."""

        model = MinMaxValidationRule
        fields = ["name", "enabled", "content_type", "field", "min", "max", "error_message", "tags"]


class MinMaxValidationRuleBulkEditForm(NautobotBulkEditForm, TagsBulkEditFormMixin):
    """Base bulk edit form for the MinMaxValidationRule model."""

    pk = DynamicModelMultipleChoiceField(queryset=MinMaxValidationRule.objects.all(), widget=forms.MultipleHiddenInput)
    enabled = forms.NullBooleanField(
        required=False,
        widget=BulkEditNullBooleanSelect(),
    )
    min = forms.IntegerField(required=False)
    max = forms.IntegerField(required=False)
    error_message = forms.CharField(required=False)

    class Meta:
        """Bulk edit form metadata for the MinMaxValidationRule model."""

        fields = ["tags"]
        nullable_fields = ["error_message"]


class MinMaxValidationRuleFilterForm(NautobotFilterForm):
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
    tag = TagFilterField(model)


#
# RequiredValidationRules
#


class RequiredValidationRuleForm(NautobotModelForm):
    """Base model form for the RequiredValidationRule model."""

    content_type = DynamicModelChoiceField(
        queryset=ContentType.objects.filter(FeatureQuery("custom_validators").get_query()).order_by(
            "app_label", "model"
        ),
    )

    class Meta:
        """Form metadata for the RequiredValidationRule model."""

        model = RequiredValidationRule
        fields = [
            "name",
            "enabled",
            "content_type",
            "field",
            "error_message",
            "tags",
        ]


class RequiredValidationRuleBulkEditForm(NautobotBulkEditForm, TagsBulkEditFormMixin):
    """Base bulk edit form for the RequiredValidationRule model."""

    pk = DynamicModelMultipleChoiceField(queryset=RequiredValidationRule.objects.all(), widget=forms.MultipleHiddenInput)
    enabled = forms.NullBooleanField(
        required=False,
        widget=BulkEditNullBooleanSelect(),
    )
    error_message = forms.CharField(required=False)

    class Meta:
        """Bulk edit form metadata for the RequiredValidationRule model."""

        fields = ["tags"]
        nullable_fields = ["error_message"]


class RequiredValidationRuleFilterForm(NautobotFilterForm):
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
    tag = TagFilterField(model)


#
# UniqueValidationRules
#


class UniqueValidationRuleForm(NautobotModelForm):
    """Base model form for the UniqueValidationRule model."""

    content_type = DynamicModelChoiceField(
        queryset=ContentType.objects.filter(FeatureQuery("custom_validators").get_query()).order_by(
            "app_label", "model"
        ),
    )

    class Meta:
        """Form metadata for the UniqueValidationRule model."""

        model = UniqueValidationRule
        fields = [
            "name",
            "enabled",
            "content_type",
            "field",
            "max_instances",
            "error_message",
            "tags",
        ]


class UniqueValidationRuleBulkEditForm(NautobotBulkEditForm, TagsBulkEditFormMixin):
    """Base bulk edit form for the UniqueValidationRule model."""

    pk = DynamicModelMultipleChoiceField(queryset=UniqueValidationRule.objects.all(), widget=forms.MultipleHiddenInput)
    enabled = forms.NullBooleanField(
        required=False,
        widget=BulkEditNullBooleanSelect(),
    )
    max_instances = forms.IntegerField(required=False)
    error_message = forms.CharField(required=False)

    class Meta:
        """Bulk edit form metadata for the UniqueValidationRule model."""

        fields = ["tags"]
        nullable_fields = ["error_message"]


class UniqueValidationRuleFilterForm(NautobotFilterForm):
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
    tag = TagFilterField(model)


#
# DataCompliance
#


class DataComplianceFilterForm(NautobotModelForm):
    """Form for DataCompliance instances."""

    model = DataCompliance
    compliance_class_name = forms.CharField(max_length=20, required=False)
    validated_attribute = forms.CharField(max_length=20, required=False)
    valid = forms.NullBooleanField(required=False, widget=StaticSelect2(choices=BOOLEAN_WITH_BLANK_CHOICES))
    content_type = MultipleContentTypeField(
        feature=None,
        queryset=ContentType.objects.all().order_by("app_label", "model"),
        choices_as_strings=True,
        required=False,
    )
    q = forms.CharField(required=False, label="Search")
