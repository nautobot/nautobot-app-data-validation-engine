"""Nautobot data validation engine plugin."""
__version__ = "1.0.0"

from nautobot.extras.plugins import PluginConfig


class NautobotDataValidationEngineConfig(PluginConfig):
    """Plugin configuration for the nautobot_data_validation_engine plugin."""

    name = "nautobot_data_validation_engine"
    verbose_name = "Data Validation Engine"
    version = __version__
    author = "Network to Code"
    author_email = "opensource@networktocode.com"
    description = "Plugin that provides a UI for managing custom data validation rules."
    base_url = "data-validation-engine"
    required_settings = []
    default_settings = {}
    caching_config = {}


config = NautobotDataValidationEngineConfig  # pylint: disable=invalid-name
