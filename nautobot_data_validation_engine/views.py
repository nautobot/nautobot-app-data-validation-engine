"""Django views."""

from django.apps import apps as global_apps
from django.contrib.contenttypes.models import ContentType
from django_tables2 import RequestConfig
from nautobot.core.views.viewsets import NautobotUIViewSet
from nautobot.core.views.generic import ObjectView
from nautobot.apps.views import (
    ObjectListViewMixin,
    ObjectDetailViewMixin,
    ObjectDestroyViewMixin,
    ObjectBulkDestroyViewMixin,
)
from nautobot.core.views.paginator import EnhancedPaginator, get_paginate_count

from nautobot_data_validation_engine import filters, forms, tables
from nautobot_data_validation_engine.api import serializers
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


class RegularExpressionValidationRuleUIViewSet(NautobotUIViewSet):
    """Views for the RegularExpressionValidationRule model."""

    bulk_update_form_class = forms.RegularExpressionValidationRuleBulkEditForm
    filterset_class = filters.RegularExpressionValidationRuleFilterSet
    filterset_form_class = forms.RegularExpressionValidationRuleFilterForm
    form_class = forms.RegularExpressionValidationRuleForm
    queryset = RegularExpressionValidationRule.objects.all()
    serializer_class = serializers.RegularExpressionValidationRuleSerializer
    table_class = tables.RegularExpressionValidationRuleTable


#
# MinMaxValidationRules
#


class MinMaxValidationRuleUIViewSet(NautobotUIViewSet):
    """Views for the MinMaxValidationRuleUIViewSet model."""

    bulk_update_form_class = forms.MinMaxValidationRuleBulkEditForm
    filterset_class = filters.MinMaxValidationRuleFilterSet
    filterset_form_class = forms.MinMaxValidationRuleFilterForm
    form_class = forms.MinMaxValidationRuleForm
    queryset = MinMaxValidationRule.objects.all()
    serializer_class = serializers.MinMaxValidationRuleSerializer
    table_class = tables.MinMaxValidationRuleTable


#
# RequiredValidationRules
#


class RequiredValidationRuleUIViewSet(NautobotUIViewSet):
    """Views for the RequiredValidationRuleUIViewSet model."""

    bulk_update_form_class = forms.RequiredValidationRuleBulkEditForm
    filterset_class = filters.RequiredValidationRuleFilterSet
    filterset_form_class = forms.RequiredValidationRuleFilterForm
    form_class = forms.RequiredValidationRuleForm
    queryset = RequiredValidationRule.objects.all()
    serializer_class = serializers.RequiredValidationRuleSerializer
    table_class = tables.RequiredValidationRuleTable


#
# UniqueValidationRules
#


class UniqueValidationRuleUIViewSet(NautobotUIViewSet):
    """Views for the UniqueValidationRuleUIViewSet model."""

    bulk_update_form_class = forms.UniqueValidationRuleBulkEditForm
    filterset_class = filters.UniqueValidationRuleFilterSet
    filterset_form_class = forms.UniqueValidationRuleFilterForm
    form_class = forms.UniqueValidationRuleForm
    queryset = UniqueValidationRule.objects.all()
    serializer_class = serializers.UniqueValidationRuleSerializer
    table_class = tables.UniqueValidationRuleTable


#
# DataCompliance
#


class DataComplianceListView(  # pylint: disable=W0223
    ObjectListViewMixin, ObjectDetailViewMixin, ObjectDestroyViewMixin, ObjectBulkDestroyViewMixin
):
    """Views for the DataComplianceListView model."""

    lookup_field = "pk"
    queryset = DataCompliance.objects.all()
    table_class = tables.DataComplianceTable
    filterset_class = filters.DataComplianceFilterSet
    filterset_form_class = forms.DataComplianceFilterForm
    serializer_class = serializers.DataComplianceSerializer
    action_buttons = ("export",)


class DataComplianceObjectView(ObjectView):
    """View for the Audit Results tab dynamically generated on specific object detail views."""

    template_name = "nautobot_data_validation_engine/datacompliance_tab.html"

    def dispatch(self, request, *args, **kwargs):
        """Set the queryset for the given object and call the inherited dispatch method."""
        model = kwargs.pop("model")
        if not self.queryset:
            self.queryset = global_apps.get_model(model).objects.all()
        return super().dispatch(request, *args, **kwargs)

    def get_extra_context(self, request, instance):
        """Generate extra context for rendering the DataComplianceObjectView template."""
        compliance_objects = DataCompliance.objects.filter(
            content_type=ContentType.objects.get_for_model(instance), object_id=instance.id
        )
        compliance_table = tables.DataComplianceTableTab(compliance_objects)

        paginate = {"paginator_class": EnhancedPaginator, "per_page": get_paginate_count(request)}
        RequestConfig(request, paginate).configure(compliance_table)
        return {"active_tab": request.GET["tab"], "table": compliance_table}
