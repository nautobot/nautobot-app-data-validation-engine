"""
Django url patterns.
"""
from django.urls import path, include

from nautobot.extras.views import ObjectChangeLogView

from nautobot_data_validation_engine import views
from nautobot_data_validation_engine.models import MinMaxValidationRule, RegularExpressionValidationRule


rule_patterns = [
    path(
        "regex/",
        views.RegularExpressionValidationRuleListView.as_view(),
        name="regularexpressionvalidationrule_list",
    ),
    path(
        "regex/add/",
        views.RegularExpressionValidationRuleEditView.as_view(),
        name="regularexpressionvalidationrule_add",
    ),
    path(
        "regex/import/",
        views.RegularExpressionValidationRuleBulkImportView.as_view(),
        name="regularexpressionvalidationrule_import",
    ),
    path(
        "regex/edit/",
        views.RegularExpressionValidationRuleBulkEditView.as_view(),
        name="regularexpressionvalidationrule_bulk_edit",
    ),
    path(
        "regex/delete/",
        views.RegularExpressionValidationRuleBulkDeleteView.as_view(),
        name="regularexpressionvalidationrule_bulk_delete",
    ),
    path(
        "regex/<slug:slug>/",
        views.RegularExpressionValidationRuleView.as_view(),
        name="regularexpressionvalidationrule",
    ),
    path(
        "regex/<slug:slug>/edit/",
        views.RegularExpressionValidationRuleEditView.as_view(),
        name="regularexpressionvalidationrule_edit",
    ),
    path(
        "regex/<slug:slug>/delete/",
        views.RegularExpressionValidationRuleDeleteView.as_view(),
        name="regularexpressionvalidationrule_delete",
    ),
    path(
        "regex/<slug:slug>/changelog/",
        ObjectChangeLogView.as_view(),
        name="regularexpressionvalidationrule_changelog",
        kwargs={"model": RegularExpressionValidationRule},
    ),
    path(
        "min-max/",
        views.MinMaxValidationRuleListView.as_view(),
        name="minmaxvalidationrule_list",
    ),
    path(
        "min-max/add/",
        views.MinMaxValidationRuleEditView.as_view(),
        name="minmaxvalidationrule_add",
    ),
    path(
        "min-max/import/",
        views.MinMaxValidationRuleBulkImportView.as_view(),
        name="minmaxvalidationrule_import",
    ),
    path(
        "min-max/edit/",
        views.MinMaxValidationRuleBulkEditView.as_view(),
        name="minmaxvalidationrule_bulk_edit",
    ),
    path(
        "min-max/delete/",
        views.MinMaxValidationRuleBulkDeleteView.as_view(),
        name="minmaxvalidationrule_bulk_delete",
    ),
    path(
        "min-max/<slug:slug>/",
        views.MinMaxValidationRuleView.as_view(),
        name="minmaxvalidationrule",
    ),
    path(
        "min-max/<slug:slug>/edit/",
        views.MinMaxValidationRuleEditView.as_view(),
        name="minmaxvalidationrule_edit",
    ),
    path(
        "min-max/<slug:slug>/delete/",
        views.MinMaxValidationRuleDeleteView.as_view(),
        name="minmaxvalidationrule_delete",
    ),
    path(
        "min-max/<slug:slug>/changelog/",
        ObjectChangeLogView.as_view(),
        name="minmaxvalidationrule_changelog",
        kwargs={"model": MinMaxValidationRule},
    ),
]

urlpatterns = [
    path("rules/", include(rule_patterns)),
]
