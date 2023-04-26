"""Template content for nautobot_data_validation_engine."""
from django.urls import reverse
from nautobot.extras.plugins import TemplateExtension
from nautobot_data_validation_engine.models import DataCompliance


def tab_factory(content_type_label):
    """Generate a DataComplianceTab object for a given content type."""

    class DataComplianceTab(TemplateExtension):  # pylint: disable=W0223
        """Dynamically generated DataComplianceTab class."""

        model = content_type_label

        def detail_tabs(self):
            app_label, model = self.model.split(".")
            return (
                [
                    {
                        "title": "Data Compliance",
                        "url": reverse(
                            "plugins:nautobot_data_validation_engine:data-compliance-tab",
                            kwargs={"id": self.context["object"].id, "model": self.model},
                        ),
                    }
                ]
                if DataCompliance.objects.filter(content_type__app_label=app_label, content_type__model=model).exists()
                else []
            )

    return DataComplianceTab


template_extensions = []
