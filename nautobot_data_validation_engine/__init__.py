"""Plugin declaration for nautobot_data_validation_engine."""
# Metadata is inherited from Nautobot. If not including Nautobot in the environment, this should be added
try:
    from importlib import metadata
except ImportError:
    # Python version < 3.8
    import importlib_metadata as metadata

__version__ = metadata.version(__name__)

import logging
from nautobot.extras.plugins import NautobotAppConfig

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
    max_version = "2.9999"
    default_settings = {}
    caching_config = {}


config = NautobotDataValidationEngineConfig  # pylint:disable=invalid-name
