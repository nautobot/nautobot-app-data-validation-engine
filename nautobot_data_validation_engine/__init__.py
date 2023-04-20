"""Plugin declaration for nautobot_data_validation_engine."""
# Metadata is inherited from Nautobot. If not including Nautobot in the environment, this should be added
try:
    from importlib import metadata
except ImportError:
    # Python version < 3.8
    import importlib_metadata as metadata

__version__ = metadata.version(__name__)

import logging
from django.db.utils import ProgrammingError
from nautobot.extras.plugins import NautobotAppConfig, register_template_extensions
from nautobot.extras.plugins.utils import import_object

logger = logging.getLogger(__name__)


class NautobotDataValidationEngineConfig(NautobotAppConfig):
    """Plugin configuration for the nautobot_data_validation_engine plugin."""

    name = "nautobot_data_validation_engine"
    verbose_name = "Data Validation Engine"
    version = __version__
    author = "Network to Code, LLC"
    description = "Provides UI to build custom data validation rules for data in Nautobot."
    base_url = "nautobot-data-validation-engine"
    required_settings = []
    min_version = "1.5.2"
    max_version = "1.9999"
    default_settings = {}
    caching_config = {}
    audit_rulesets = "audit_rulesets.audit_rulesets"

    def ready(self):
        super().ready()
        from nautobot_data_validation_engine.template_content import tab_factory  # pylint: disable=C0415
        from django.contrib.contenttypes.models import ContentType  # pylint: disable=C0415

        audit_rulesets = import_object(f"{self.__module__}.{self.audit_rulesets}")
        if audit_rulesets is not None:
            self.features["audit_rulesets"] = sorted(set(audit_ruleset.model for audit_ruleset in audit_rulesets))
            template_content = []
            labels = []
            try:
                for content_type in ContentType.objects.all():
                    label = f"{content_type.app_label}.{content_type.model}"
                    labels.append(label)
                    template_content.append(tab_factory(label))
                register_template_extensions(template_content)
                self.features["template_extensions"] = sorted(set(labels))
            except ProgrammingError:
                logger.warning(
                    "Creating template content for validation engine failed because "
                    "the ContentType table was not available or populated. This is normal "
                    "during the execution of the migration command for the first time."
                )


config = NautobotDataValidationEngineConfig  # pylint:disable=invalid-name
