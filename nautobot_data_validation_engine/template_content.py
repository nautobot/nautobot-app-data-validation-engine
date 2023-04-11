"""Template content for nautobot_data_validation_engine."""
from django.conf import settings
from django.urls import reverse
from nautobot.extras.plugins import TemplateExtension
from nautobot_data_validation_engine.models import ValidationResult

PLUGIN_CFG = settings.PLUGINS_CONFIG["nautobot_data_validation_engine"]


def tab_factory(content_type_label):
    """Generate a ValidationTab object for a given content type."""

    class ValidationTab(TemplateExtension):  # pylint: disable=W0223
        """Dynamically generated ValidationTab class."""

        model = content_type_label

        def __determine_visibility(self):
            app_label, model = self.model.split(".")
            visibility = PLUGIN_CFG["VALIDATION_TAB_VISIBILITY"].upper()
            if visibility == "MODEL":
                return ValidationResult.objects.filter(
                    content_type__app_label=app_label, content_type__model=model
                ).exists()
            if visibility == "INSTANCE":
                return ValidationResult.objects.filter(
                    content_type__app_label=app_label, content_type__model=model, object_id=self.context["object"].id
                ).exists()
            return True

        def detail_tabs(self):
            return (
                [
                    {
                        "title": "Validations",
                        "url": reverse(
                            "plugins:nautobot_data_validation_engine:validationresults",
                            kwargs={"id": self.context["object"].id, "model": self.model},
                        ),
                    }
                ]
                if self.__determine_visibility()
                else []
            )

    return ValidationTab


template_extensions = []
