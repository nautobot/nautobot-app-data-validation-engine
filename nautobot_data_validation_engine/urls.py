"""
Django url patterns.
"""
from django.urls import path

from nautobot.extras.views import ObjectChangeLogView

from nautobot_data_validation_engine import views
from nautobot_data_validation_engine.models import MinMaxValidationRule, RegularExpressionValidationRule


urlpatterns = [
    path(
        "regex-rules/",
        views.RegularExpressionValidationRuleListView.as_view(),
        name="regularexpressionvalidationrule_list",
    ),
    path(
        "regex-rules/add/",
        views.RegularExpressionValidationRuleEditView.as_view(),
        name="regularexpressionvalidationrule_add",
    ),
    path(
        "regex-rules/import/",
        views.RegularExpressionValidationRuleBulkImportView.as_view(),
        name="regularexpressionvalidationrule_import",
    ),
    path(
        "regex-rules/edit/",
        views.RegularExpressionValidationRuleBulkEditView.as_view(),
        name="regularexpressionvalidationrule_bulk_edit",
    ),
    path(
        "regex-rules/delete/",
        views.RegularExpressionValidationRuleBulkDeleteView.as_view(),
        name="regularexpressionvalidationrule_bulk_delete",
    ),
    path(
        "regex-rules/<uuid:pk>/",
        views.RegularExpressionValidationRuleView.as_view(),
        name="regularexpressionvalidationrule",
    ),
    path(
        "regex-rules/<uuid:pk>/edit/",
        views.RegularExpressionValidationRuleEditView.as_view(),
        name="regularexpressionvalidationrule_edit",
    ),
    path(
        "regex-rules/<uuid:pk>/delete/",
        views.RegularExpressionValidationRuleDeleteView.as_view(),
        name="regularexpressionvalidationrule_delete",
    ),
    path(
        "regex-rules/<uuid:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="regularexpressionvalidationrule_changelog",
        kwargs={"model": RegularExpressionValidationRule},
    ),
    path(
        "min-max-rules/",
        views.MinMaxValidationRuleListView.as_view(),
        name="minmaxvalidationrule_list",
    ),
    path(
        "min-max-rules/add/",
        views.MinMaxValidationRuleEditView.as_view(),
        name="minmaxvalidationrule_add",
    ),
    path(
        "min-max-rules/import/",
        views.MinMaxValidationRuleBulkImportView.as_view(),
        name="minmaxvalidationrule_import",
    ),
    path(
        "min-max-rules/edit/",
        views.MinMaxValidationRuleBulkEditView.as_view(),
        name="minmaxvalidationrule_bulk_edit",
    ),
    path(
        "min-max-rules/delete/",
        views.MinMaxValidationRuleBulkDeleteView.as_view(),
        name="minmaxvalidationrule_bulk_delete",
    ),
    path(
        "min-max-rules/<uuid:pk>/",
        views.MinMaxValidationRuleView.as_view(),
        name="minmaxvalidationrule",
    ),
    path(
        "min-max-rules/<uuid:pk>/edit/",
        views.MinMaxValidationRuleEditView.as_view(),
        name="minmaxvalidationrule_edit",
    ),
    path(
        "min-max-rules/<uuid:pk>/delete/",
        views.MinMaxValidationRuleDeleteView.as_view(),
        name="minmaxvalidationrule_delete",
    ),
    path(
        "min-max-rules/<uuid:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="minmaxvalidationrule_changelog",
        kwargs={"model": MinMaxValidationRule},
    ),
]
