"""
Django forms.
"""
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
)

from nautobot_data_validation_engine.models import RegularExpressionValidationRule


#
# RegularExpressionValidationRules
#


class RegularExpressionValidationRuleForm(BootstrapMixin, forms.ModelForm):
    """
    Base model form for the RegularExpressionValidationRule model.
    """

    content_type = forms.ModelChoiceField(
        queryset=ContentType.objects.filter(FeatureQuery("custom_validators").get_query()).order_by(
            "app_label", "model"
        ),
    )

    class Meta:
        model = RegularExpressionValidationRule
        fields = ["name", "enabled", "content_type", "field", "regular_expression", "error_message"]


class RegularExpressionValidationRuleCSVForm(CSVModelForm):
    """
    Base csv form for the RegularExpressionValidationRule model.
    """

    content_type = CSVContentTypeField(
        queryset=ContentType.objects.filter(FeatureQuery("custom_validators").get_query()),
        help_text="The object type to which this regular expression rule applies.",
    )

    class Meta:
        model = RegularExpressionValidationRule
        fields = RegularExpressionValidationRule.csv_headers


class RegularExpressionValidationRuleBulkEditForm(BootstrapMixin, BulkEditForm):
    """
    Base bulk edit form for the RegularExpressionValidationRule model.
    """

    pk = forms.ModelMultipleChoiceField(
        queryset=RegularExpressionValidationRule.objects.all(), widget=forms.MultipleHiddenInput
    )
    enabled = forms.NullBooleanField(
        required=False,
        widget=BulkEditNullBooleanSelect(),
    )
    regular_expression = forms.CharField(required=False)
    error_message = forms.CharField(required=False)

    class Meta:
        nullable_fields = ["error_message"]


class RegularExpressionValidationRuleFilterForm(BootstrapMixin, forms.Form):
    """
    Base filter form for the RegularExpressionValidationRule model.
    """

    model = RegularExpressionValidationRule
    field_order = ["q", "name", "enabled", "content_type", "field", "regular_expression", "error_message"]
    q = forms.CharField(required=False, label="Search")
    # "CSV" field is being used here because it is using the slug-form input for
    # content-types, which improves UX.
    content_type = CSVMultipleContentTypeField(
        queryset=ContentType.objects.filter(FeatureQuery("custom_validators").get_query()).order_by(
            "app_label", "model"
        ),
        required=False,
    )
