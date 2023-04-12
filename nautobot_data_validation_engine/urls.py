"""Django url patterns."""

from django.urls import path

from nautobot.core.views.routers import NautobotUIViewSetRouter
from nautobot.extras.views import ObjectChangeLogView, ObjectNotesView

from nautobot_data_validation_engine import views, models


router = NautobotUIViewSetRouter()
router.register("audit-rule", views.AuditRuleListView)
router.register("regex-rules", views.RegularExpressionValidationRuleUIViewSet)
router.register("min-max-rules", views.MinMaxValidationRuleUIViewSet)
router.register("required-rules", views.RequiredValidationRuleUIViewSet)
router.register("unique-rules", views.UniqueValidationRuleUIViewSet)

urlpatterns = [
    path(
        "audit-rules/<model>/<id>/",
        views.AuditRuleObjectView.as_view(),
        name="auditrules",
    ),
    path(
        "audit-rule/<uuid:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="auditrule_changelog",
        kwargs={"model": models.AuditRule},
    ),
    path(
        "audit-rule/<uuid:pk>/notes/",
        ObjectNotesView.as_view(),
        name="auditrule_notes",
        kwargs={"model": models.AuditRule},
    ),
    path(
        "regex-rules/<uuid:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="regularexpressionvalidationrule_changelog",
        kwargs={"model": models.RegularExpressionValidationRule},
    ),
    path(
        "regex-rules/<uuid:pk>/notes/",
        ObjectNotesView.as_view(),
        name="regularexpressionvalidationrule_notes",
        kwargs={"model": models.RegularExpressionValidationRule},
    ),
    path(
        "min-max-rules/<uuid:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="minmaxvalidationrule_changelog",
        kwargs={"model": models.MinMaxValidationRule},
    ),
    path(
        "min-max-rules/<uuid:pk>/notes/",
        ObjectNotesView.as_view(),
        name="minmaxvalidationrule_notes",
        kwargs={"model": models.MinMaxValidationRule},
    ),
    path(
        "required-rules/<uuid:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="requiredvalidationrule_changelog",
        kwargs={"model": models.RequiredValidationRule},
    ),
    path(
        "required-rules/<uuid:pk>/notes/",
        ObjectNotesView.as_view(),
        name="requiredvalidationrule_notes",
        kwargs={"model": models.RequiredValidationRule},
    ),
    path(
        "unique-rules/<uuid:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="uniquevalidationrule_changelog",
        kwargs={"model": models.UniqueValidationRule},
    ),
    path(
        "unique-rules/<uuid:pk>/notes/",
        ObjectNotesView.as_view(),
        name="uniquevalidationrule_notes",
        kwargs={"model": models.UniqueValidationRule},
    ),
] + router.urls
