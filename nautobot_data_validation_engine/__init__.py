"""Nautobot data validation engine plugin."""
from nautobot.extras.plugins import PluginConfig

try:
    from importlib import metadata
except ImportError:
    # Python version < 3.8
    import importlib_metadata as metadata

__version__ = metadata.version(__name__)


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
    min_version = "1.5.0"
    max_version = "1.9999"
    default_settings = {}
    caching_config = {}


config = NautobotDataValidationEngineConfig  # pylint: disable=invalid-name
