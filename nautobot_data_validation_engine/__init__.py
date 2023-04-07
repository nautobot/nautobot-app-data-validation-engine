"""Plugin declaration for nautobot_data_validation_engine."""
# Metadata is inherited from Nautobot. If not including Nautobot in the environment, this should be added
try:
    from importlib import metadata
except ImportError:
    # Python version < 3.8
    import importlib_metadata as metadata

__version__ = metadata.version(__name__)

from nautobot.extras.plugins import PluginConfig
import inspect
import collections


class NautobotDataValidationEngineConfig(PluginConfig):
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

    def ready(self):
        super().ready()
        from nautobot.extras.utils import registry

        registry["plugin_validations"] = collections.defaultdict(list)
        validations = import_object(f"{self.__module__}.{self.validations}")
        if validations is not None:
            register_validations(validations)
            self.features["validations"] = sorted(set(validation.model for validation in validations))


def register_validations(class_list):
    from nautobot.extras.utils import registry
    from nautobot_data_validation_engine.validations import ValidationSet

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


config = NautobotDataValidationEngineConfig  # pylint:disable=invalid-name
