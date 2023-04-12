"""Template content for nautobot_data_validation_engine."""
from django.urls import reverse
from nautobot.extras.plugins import TemplateExtension
from nautobot_data_validation_engine.models import ValidationResult


def tab_factory(content_type_label):
    """Generate a ValidationTab object for a given content type."""

    class ValidationTab(TemplateExtension):  # pylint: disable=W0223
        """Dynamically generated ValidationTab class."""

        model = content_type_label

        def detail_tabs(self):
            app_label, model = self.model.split(".")
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
                if ValidationResult.objects.filter(
                    content_type__app_label=app_label, content_type__model=model
                ).exists()
                else []
            )

    return ValidationTab


template_extensions = []
