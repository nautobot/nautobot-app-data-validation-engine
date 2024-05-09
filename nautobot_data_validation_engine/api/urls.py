"""API routes."""

from nautobot.core.api.routers import OrderedDefaultRouter

from nautobot_data_validation_engine.api import views


router = OrderedDefaultRouter(view_name="Data Validation Engine")

# Regular expression rules
router.register("regex-rules", views.RegularExpressionValidationRuleViewSet)

# Min/max rules
router.register("min-max-rules", views.MinMaxValidationRuleViewSet)

# Required rules
router.register("required-rules", views.RequiredValidationRuleViewSet)

# Unique rules
router.register("unique-rules", views.UniqueValidationRuleViewSet)

# Data Compliance
router.register("data-compliance", views.DataComplianceAPIView)


urlpatterns = router.urls
