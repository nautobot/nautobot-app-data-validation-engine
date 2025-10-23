"""Django urlpatterns declaration for nautobot_data_validation_engine app."""

from django.templatetags.static import static
from django.urls import path
from django.views.generic import RedirectView
from nautobot.apps.urls import NautobotUIViewSetRouter


from nautobot_data_validation_engine import views


app_name = "nautobot_data_validation_engine"
router = NautobotUIViewSetRouter()

# The standard is for the route to be the hyphenated version of the model class name plural.
# for example, ExampleModel would be example-models.
router.register("regular-expression-validation-rules", views.RegularExpressionValidationRuleUIViewSet)


urlpatterns = [
    path("docs/", RedirectView.as_view(url=static("nautobot_data_validation_engine/docs/index.html")), name="docs"),
]

urlpatterns += router.urls
