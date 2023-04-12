"""Template content for nautobot_data_validation_engine."""
from django.urls import reverse
from nautobot.extras.plugins import TemplateExtension
from nautobot_data_validation_engine.models import AuditRule


def tab_factory(content_type_label):
    """Generate a AuditRuleTab object for a given content type."""

    class AuditRuleTab(TemplateExtension):  # pylint: disable=W0223
        """Dynamically generated AuditRuleTab class."""

        model = content_type_label

        def detail_tabs(self):
            app_label, model = self.model.split(".")
            return (
                [
                    {
                        "title": "Audit Rules",
                        "url": reverse(
                            "plugins:nautobot_data_validation_engine:auditrules",
                            kwargs={"id": self.context["object"].id, "model": self.model},
                        ),
                    }
                ]
                if AuditRule.objects.filter(content_type__app_label=app_label, content_type__model=model).exists()
                else []
            )

    return AuditRuleTab


template_extensions = []
