"""Template content for nautobot_data_validation_engine."""
from nautobot.extras.plugins import TemplateExtension
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse


def tab_factory(content_type):
    """Generate a ValidationTab object for a given content type."""

    class ValidationTab(TemplateExtension):
        model = content_type

        def detail_tabs(self):
            return [
                {
                    "title": "Validations",
                    "url": reverse(
                        "plugins:nautobot_data_validation_engine:validationresults",
                        kwargs={"id": self.context["object"].id, "model": self.model},
                    ),
                }
            ]

    return ValidationTab


template_extensions = []
for content_type in ContentType.objects.all():
    class_instance = tab_factory(f"{content_type.app_label}.{content_type.model}")
    template_extensions.append(class_instance)
