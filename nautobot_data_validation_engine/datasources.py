"""Datasource definitions."""
import importlib
from nautobot.extras.choices import LogLevelChoices
from nautobot.extras.registry import DatasourceContent


def refresh_git_audit_ruleset(repository_record, job_result, delete=False):  # pylint: disable=W0613
    """Callback for repo refresh."""
    job_result.log("Successfully pulled git repo", level_choice=LogLevelChoices.LOG_SUCCESS)
    spec = importlib.util.spec_from_file_location(
        "custom_validators", f"{repository_record.filesystem_path}/custom_validators.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if hasattr(module, "custom_validators"):
        for audit_class in module.custom_validators:
            job_result.log(f"Found class {str(audit_class.__name__)}", level_choice=LogLevelChoices.LOG_SUCCESS)


datasource_contents = [
    (
        "extras.gitrepository",
        DatasourceContent(
            name="audit rulesets",
            content_identifier="nautobot_data_validation_engine.audit_rulesets",
            icon="mdi-file-document-outline",
            callback=refresh_git_audit_ruleset,
        ),
    )
]
