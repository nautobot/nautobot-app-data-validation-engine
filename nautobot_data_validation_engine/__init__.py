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
    description = "Nautobot App that provides a data validation rules engine to easily codify data standards in the UI. Includes RegEx and Min/Max validation rules."
    base_url = "data-validation-engine"
    required_settings = []
    default_settings = {}
    caching_config = {}


config = NautobotDataValidationEngineConfig  # pylint: disable=invalid-name
