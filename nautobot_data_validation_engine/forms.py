"""Forms for nautobot_data_validation_engine."""

from django import forms
from nautobot.apps.constants import CHARFIELD_MAX_LENGTH
from nautobot.apps.forms import NautobotBulkEditForm, NautobotFilterForm, NautobotModelForm, TagsBulkEditFormMixin

from nautobot_data_validation_engine import models


class ValidationRuleForm(NautobotModelForm):  # pylint: disable=too-many-ancestors
    """ValidationRule creation/edit form."""

    class Meta:
        """Meta attributes."""

        model = models.ValidationRule
        fields = "__all__"


class ValidationRuleBulkEditForm(TagsBulkEditFormMixin, NautobotBulkEditForm):  # pylint: disable=too-many-ancestors
    """ValidationRule bulk edit form."""

    pk = forms.ModelMultipleChoiceField(queryset=models.ValidationRule.objects.all(), widget=forms.MultipleHiddenInput)
    description = forms.CharField(required=False, max_length=CHARFIELD_MAX_LENGTH)

    class Meta:
        """Meta attributes."""

        nullable_fields = [
            "description",
        ]


class ValidationRuleFilterForm(NautobotFilterForm):
    """Filter form to filter searches."""

    model = models.ValidationRule
    field_order = ["q", "name"]

    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name.",
    )
    name = forms.CharField(required=False, label="Name")
