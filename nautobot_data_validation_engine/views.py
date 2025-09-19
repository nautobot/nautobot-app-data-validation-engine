"""Views for nautobot_data_validation_engine."""

from nautobot.apps.views import NautobotUIViewSet

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
