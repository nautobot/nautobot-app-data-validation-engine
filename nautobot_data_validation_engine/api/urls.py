"""API routes."""

from nautobot.core.api import OrderedDefaultRouter

from nautobot_data_validation_engine.api import views


router = OrderedDefaultRouter()
router.APIRootView = views.DataValidationEngineRootView

# Regular expression rules
router.register("regex-rules", views.RegularExpressionValidationRuleViewSet)

# Min/max rules
router.register("min-max-rules", views.MinMaxValidationRuleViewSet)

# Required rules
router.register("required-rules", views.RequiredValidationRuleViewSet)

# Unique rules
router.register("unique-rules", views.UniqueValidationRuleViewSet)

router.register("audit-rules", views.AuditResultAPIView)


urlpatterns = router.urls
