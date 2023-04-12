"""Plugin declaration for nautobot_data_validation_engine."""
# Metadata is inherited from Nautobot. If not including Nautobot in the environment, this should be added
try:
    from importlib import metadata
except ImportError:
    # Python version < 3.8
    import importlib_metadata as metadata

__version__ = metadata.version(__name__)

import inspect
import collections
import logging
from django.db.utils import ProgrammingError
from nautobot.extras.plugins import NautobotAppConfig, register_template_extensions
from nautobot.extras.plugins.utils import import_object

CHOICES = []

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
    default_settings = {
        "VALIDATION_TAB_VISIBILITY": "ALWAYS"
    }
    caching_config = {}
    validations = "validations.validations"

    def ready(self):
        """Call the ready function and add validations to the registry"""
        super().ready()
        from nautobot.extras.utils import registry  # pylint: disable=C0415
        from nautobot_data_validation_engine.template_content import tab_factory  # pylint: disable=C0415
        from django.contrib.contenttypes.models import ContentType  # pylint: disable=C0415

        registry["plugin_validations"] = collections.defaultdict(list)
        validations = import_object(f"{self.__module__}.{self.validations}")
        if validations is not None:
            register_validations(validations)
            self.features["validations"] = sorted(set(validation.model for validation in validations))
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


def register_validations(class_list):
    """Register ValidationSet classes to the registry."""
    from nautobot.extras.utils import registry  # pylint: disable=C0415
    from nautobot_data_validation_engine.validations import ValidationSet  # pylint: disable=C0415

    for validation in class_list:
        if not inspect.isclass(validation):
            raise TypeError(f"ValidationSet class {validation} was passed as an instance!")
        if not issubclass(validation, ValidationSet):
            raise TypeError(
                f"{validation} is not a subclass of nautobot_data_validation_engine.validations.ValidationSet!"
            )
        if validation.model is None:
            raise TypeError(f"ValidationSet class {validation} does not declare a valid model!")
        registry["plugin_validations"][validation.model].append(validation)
        CHOICES.append((validation.__name__, validation.__name__))
    CHOICES.sort()


config = NautobotDataValidationEngineConfig  # pylint:disable=invalid-name
