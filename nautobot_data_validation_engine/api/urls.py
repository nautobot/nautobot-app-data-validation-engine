"""
API routes
"""
from nautobot.core.api import OrderedDefaultRouter

from nautobot_data_validation_engine.api import views


router = OrderedDefaultRouter()
router.APIRootView = views.DataValidationEngineRootView

# Regular expression rules
router.register("regex-rules", views.RegularExpressionValidationRuleViewSet)

# Min/max expression rules
router.register("min-max-rules", views.MinMaxValidationRuleViewSet)


urlpatterns = router.urls
