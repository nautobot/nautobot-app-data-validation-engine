"""App declaration for nautobot_data_validation_engine."""

# Metadata is inherited from Nautobot. If not including Nautobot in the environment, this should be added
from importlib import metadata

from nautobot.apps import NautobotAppConfig

__version__ = metadata.version(__name__)


class NautobotDataValidationEngineConfig(NautobotAppConfig):
    """App configuration for the nautobot_data_validation_engine app."""

    name = "nautobot_data_validation_engine"
    verbose_name = "Data Validation Engine"
    version = __version__
    author = "Network to Code, LLC"
    description = "Provides UI to build custom data validation rules for data in Nautobot."
    base_url = "nautobot-data-validation-engine"
    required_settings = []
    min_version = "2.2.0"
    max_version = "2.9999"
    default_settings = {}
    caching_config = {}


config = NautobotDataValidationEngineConfig  # pylint:disable=invalid-name
