"""Django views."""

from django.contrib.contenttypes.models import ContentType
from django_tables2 import RequestConfig
from nautobot.core.views.viewsets import NautobotUIViewSet
from nautobot.core.views.generic import ObjectView
from nautobot.apps.views import ObjectListViewMixin, ObjectDetailViewMixin
from nautobot.utilities.paginator import EnhancedPaginator, get_paginate_count

from nautobot_data_validation_engine import filters, forms, tables
from nautobot_data_validation_engine.api import serializers
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


class RegularExpressionValidationRuleUIViewSet(NautobotUIViewSet):
    """Views for the RegularExpressionValidationRule model."""

    bulk_create_form_class = forms.RegularExpressionValidationRuleCSVForm
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

    bulk_create_form_class = forms.MinMaxValidationRuleCSVForm
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

    bulk_create_form_class = forms.RequiredValidationRuleCSVForm
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

    bulk_create_form_class = forms.UniqueValidationRuleCSVForm
    bulk_update_form_class = forms.UniqueValidationRuleBulkEditForm
    filterset_class = filters.UniqueValidationRuleFilterSet
    filterset_form_class = forms.UniqueValidationRuleFilterForm
    form_class = forms.UniqueValidationRuleForm
    queryset = UniqueValidationRule.objects.all()
    serializer_class = serializers.UniqueValidationRuleSerializer
    table_class = tables.UniqueValidationRuleTable


class ValidationResultListView(ObjectListViewMixin, ObjectDetailViewMixin):
    lookup_field = "pk"
    queryset = ValidationResult.objects.all()
    table_class = tables.AllValidationResultTable
    filterset_class = filters.ValidationResultFilterSet
    serializer_class = serializers.ValidationResultSerializer
    action_buttons = ("export",)


class ValidationResultObjectView(ObjectView):
    template_name = "nautobot_data_validation_engine/validationresult_retrieve.html"

    def get_extra_context(self, request, instance):
        validations = ValidationResult.objects.filter(
            content_type=ContentType.objects.get_for_model(instance), object_id=instance.id
        )
        validation_table = tables.ValidationResultTable(validations)

        paginate = {"paginator_class": EnhancedPaginator, "per_page": get_paginate_count(request)}
        RequestConfig(request, paginate).configure(validation_table)
        return {"active_tab": request.GET["tab"], "table": validation_table}
