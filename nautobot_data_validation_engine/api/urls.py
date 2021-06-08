"""
API routes
"""
from nautobot.core.api import OrderedDefaultRouter

from nautobot_data_validation_engine.api import views


router = OrderedDefaultRouter()
router.APIRootView = views.DataValidationEngineRootView

# Regular expression rules
router.register("rules/regex", views.RegularExpressionValidationRuleViewSet)

# Min/max rules
router.register("rules/min-max", views.MinMaxValidationRuleViewSet)


urlpatterns = router.urls
