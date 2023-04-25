"""Template content for nautobot_data_validation_engine."""
from django.urls import reverse
from nautobot.extras.plugins import TemplateExtension
from nautobot_data_validation_engine.models import Audit


def tab_factory(content_type_label):
    """Generate a AuditTab object for a given content type."""

    class AuditTab(TemplateExtension):  # pylint: disable=W0223
        """Dynamically generated AuditTab class."""

        model = content_type_label

        def detail_tabs(self):
            app_label, model = self.model.split(".")
            return (
                [
                    {
                        "title": "Audit",
                        "url": reverse(
                            "plugins:nautobot_data_validation_engine:audits",
                            kwargs={"id": self.context["object"].id, "model": self.model},
                        ),
                    }
                ]
                if Audit.objects.filter(content_type__app_label=app_label, content_type__model=model).exists()
                else []
            )

    return AuditTab


template_extensions = []
