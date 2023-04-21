"""Utility functions for nautobot_data_validation_engine."""

import importlib
from nautobot.extras.models import GitRepository
from nautobot.extras.datasources import ensure_git_repository


def import_python_file_from_git_repo(repo: GitRepository):
    """Load python file from git repo to use in job."""
    ensure_git_repository(repo)
    spec = importlib.util.spec_from_file_location("custom_validators", f"{repo.filesystem_path}/custom_validators.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
