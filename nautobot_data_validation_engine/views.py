"""
Django views.
"""
from nautobot.core.views import generic

from nautobot_data_validation_engine import filters, forms, tables
from nautobot_data_validation_engine.models import MinMaxValidationRule, RegularExpressionValidationRule


#
# RegularExpressionValidationRules
#


class RegularExpressionValidationRuleListView(generic.ObjectListView):
    """
    Base list view for the RegularExpressionValidationRule model.
    """

    queryset = RegularExpressionValidationRule.objects.all()
    filterset = filters.RegularExpressionValidationRuleFilterSet
    filterset_form = forms.RegularExpressionValidationRuleFilterForm
    table = tables.RegularExpressionValidationRuleTable


class RegularExpressionValidationRuleView(generic.ObjectView):
    """
    Base detail view for the RegularExpressionValidationRule model.
    """

    queryset = RegularExpressionValidationRule.objects.all()


class RegularExpressionValidationRuleEditView(generic.ObjectEditView):
    """
    Base edit view for the RegularExpressionValidationRule model.
    """

    queryset = RegularExpressionValidationRule.objects.all()
    model_form = forms.RegularExpressionValidationRuleForm


class RegularExpressionValidationRuleDeleteView(generic.ObjectDeleteView):
    """
    Base delete view for the RegularExpressionValidationRule model.
    """

    queryset = RegularExpressionValidationRule.objects.all()


class RegularExpressionValidationRuleBulkImportView(generic.BulkImportView):
    """
    Base bulk import view for the RegularExpressionValidationRule model.
    """

    queryset = RegularExpressionValidationRule.objects.all()
    model_form = forms.RegularExpressionValidationRuleCSVForm
    table = tables.RegularExpressionValidationRuleTable


class RegularExpressionValidationRuleBulkEditView(generic.BulkEditView):
    """
    Base bulk edit view for the RegularExpressionValidationRule model.
    """

    queryset = RegularExpressionValidationRule.objects.all()
    filterset = filters.RegularExpressionValidationRuleFilterSet
    table = tables.RegularExpressionValidationRuleTable
    form = forms.RegularExpressionValidationRuleBulkEditForm


class RegularExpressionValidationRuleBulkDeleteView(generic.BulkDeleteView):
    """
    Base bulk delete view for the RegularExpressionValidationRule model.
    """

    queryset = RegularExpressionValidationRule.objects.all()
    filterset = filters.RegularExpressionValidationRuleFilterSet
    table = tables.RegularExpressionValidationRuleTable


#
# MinMaxValidationRules
#


class MinMaxValidationRuleListView(generic.ObjectListView):
    """
    Base list view for the MinMaxValidationRule model.
    """

    queryset = MinMaxValidationRule.objects.all()
    filterset = filters.MinMaxValidationRuleFilterSet
    filterset_form = forms.MinMaxValidationRuleFilterForm
    table = tables.MinMaxValidationRuleTable


class MinMaxValidationRuleView(generic.ObjectView):
    """
    Base detail view for the MinMaxValidationRule model.
    """

    queryset = MinMaxValidationRule.objects.all()


class MinMaxValidationRuleEditView(generic.ObjectEditView):
    """
    Base edit view for the MinMaxValidationRule model.
    """

    queryset = MinMaxValidationRule.objects.all()
    model_form = forms.MinMaxValidationRuleForm


class MinMaxValidationRuleDeleteView(generic.ObjectDeleteView):
    """
    Base delete view for the MinMaxValidationRule model.
    """

    queryset = MinMaxValidationRule.objects.all()


class MinMaxValidationRuleBulkImportView(generic.BulkImportView):
    """
    Base bulk import view for the MinMaxValidationRule model.
    """

    queryset = MinMaxValidationRule.objects.all()
    model_form = forms.MinMaxValidationRuleCSVForm
    table = tables.MinMaxValidationRuleTable


class MinMaxValidationRuleBulkEditView(generic.BulkEditView):
    """
    Base bulk edit view for the MinMaxValidationRule model.
    """

    queryset = MinMaxValidationRule.objects.all()
    filterset = filters.MinMaxValidationRuleFilterSet
    table = tables.MinMaxValidationRuleTable
    form = forms.MinMaxValidationRuleBulkEditForm


class MinMaxValidationRuleBulkDeleteView(generic.BulkDeleteView):
    """
    Base bulk delete view for the MinMaxValidationRule model.
    """

    queryset = MinMaxValidationRule.objects.all()
    filterset = filters.MinMaxValidationRuleFilterSet
    table = tables.MinMaxValidationRuleTable
