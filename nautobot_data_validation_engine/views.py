"""Views for nautobot_data_validation_engine."""

from nautobot.apps.views import NautobotUIViewSet
from nautobot.apps.ui import ObjectDetailContent, ObjectFieldsPanel, ObjectTablePanel, SectionChoices
from nautobot.core.templatetags import helpers

from nautobot_data_validation_engine import filters, forms, models, tables
from nautobot_data_validation_engine.api import serializers


class ValidationRuleUIViewSet(NautobotUIViewSet):
    """ViewSet for ValidationRule views."""

    bulk_update_form_class = forms.ValidationRuleBulkEditForm
    filterset_class = filters.ValidationRuleFilterSet
    filterset_form_class = forms.ValidationRuleFilterForm
    form_class = forms.ValidationRuleForm
    lookup_field = "pk"
    queryset = models.ValidationRule.objects.all()
    serializer_class = serializers.ValidationRuleSerializer
    table_class = tables.ValidationRuleTable

    # Here is an example of using the UI  Component Framework for the detail view.
    # More information can be found in the Nautobot documentation:
    # https://docs.nautobot.com/projects/core/en/stable/development/core/ui-component-framework/
    object_detail_content = ObjectDetailContent(
        panels=[
            ObjectFieldsPanel(
                weight=100,
                section=SectionChoices.LEFT_HALF,
                fields="__all__",
                # Alternatively, you can specify a list of field names:
                # fields=[
                #     "name",
                #     "description",
                # ],
                # Some fields may require additional configuration, we can use value_transforms
                # value_transforms={
                #     "name": [helpers.bettertitle]
                # },
            ),
            # If there is a ForeignKey or M2M with this model we can use ObjectTablePanel
            # to display them in a table format.
            # ObjectTablePanel(
                # weight=200,
                # section=SectionChoices.RIGHT_HALF,
                # table_class=tables.ValidationRuleTable,
                # You will want to filter the table using the related_name
                # filter="validationrules",
            # ),
        ],
    )
