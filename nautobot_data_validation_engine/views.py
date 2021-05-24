"""
Django views.
"""
from django.shortcuts import reverse

from nautobot.core.views import generic
from nautobot.utilities.utils import prepare_cloned_fields

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
    template_name = "nautobot_data_validation_engine/regularexpressionvalidationrule_list.html"


class RegularExpressionValidationRuleView(generic.ObjectView):
    """
    Base detail view for the RegularExpressionValidationRule model.
    """

    queryset = RegularExpressionValidationRule.objects.all()
    template_name = "nautobot_data_validation_engine/regularexpressionvalidationrule.html"

    def get_extra_context(self, request, instance):
        """
        Generate the urls for the UI buttons since the core templatetags do not understand the plugins namespace.
        """
        clone_url = reverse("plugins:nautobot_data_validation_engine:regularexpressionvalidationrule_add")
        cloned_param_string = prepare_cloned_fields(instance)
        if cloned_param_string:
            clone_url = f"{clone_url}?{cloned_param_string}"

        edit_url = reverse(
            "plugins:nautobot_data_validation_engine:regularexpressionvalidationrule_edit", args=[instance.pk]
        )
        delete_url = reverse(
            "plugins:nautobot_data_validation_engine:regularexpressionvalidationrule_delete", args=[instance.pk]
        )

        return {
            "clone_url": clone_url,
            "edit_url": edit_url,
            "delete_url": delete_url,
        }


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
    template_name = "nautobot_data_validation_engine/minmaxvalidationrule_list.html"


class MinMaxValidationRuleView(generic.ObjectView):
    """
    Base detail view for the MinMaxValidationRule model.
    """

    queryset = MinMaxValidationRule.objects.all()
    template_name = "nautobot_data_validation_engine/minmaxvalidationrule.html"

    def get_extra_context(self, request, instance):
        """
        Generate the urls for the UI buttons since the core templatetags do not understand the plugins namespace.
        """
        clone_url = reverse("plugins:nautobot_data_validation_engine:minmaxvalidationrule_add")
        cloned_param_string = prepare_cloned_fields(instance)
        if cloned_param_string:
            clone_url = f"{clone_url}?{cloned_param_string}"

        edit_url = reverse("plugins:nautobot_data_validation_engine:minmaxvalidationrule_edit", args=[instance.pk])
        delete_url = reverse("plugins:nautobot_data_validation_engine:minmaxvalidationrule_delete", args=[instance.pk])

        return {
            "clone_url": clone_url,
            "edit_url": edit_url,
            "delete_url": delete_url,
        }


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
