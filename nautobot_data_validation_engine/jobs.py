"""Jobs for nautobot_data_validation_engine."""
import importlib
from nautobot.extras.jobs import Job, MultiChoiceVar
from nautobot.extras.utils import registry
from nautobot.extras.models import GitRepository
from nautobot.extras.datasources.git import ensure_git_repository


def import_python_file_from_git_repo(repo: GitRepository):
    """Load python file from git repo to use in job."""
    ensure_git_repository(repo)
    spec = importlib.util.spec_from_file_location("audit_rulesets", f"{repo.filesystem_path}/audit_rulesets.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def get_choices():
    """Get choices from registry."""
    choices = []
    for classes in registry["plugin_audit_rulesets"].values():
        for audit_class in classes:
            choices.append((audit_class.__name__, audit_class.__name__))
    for repo in GitRepository.objects.all():
        if "nautobot_data_validation_engine.audit_rulesets" in repo.provided_contents:
            module = import_python_file_from_git_repo(repo)
            if hasattr(module, "audit_rulesets"):
                for audit_class in module.audit_rulesets:
                    choices.append((audit_class.__name__, audit_class.__name__))
    choices.sort()
    return choices


class RunRegisteredAuditRulesets(Job):
    """Run the validate function on all registered AuditRuleset classes."""

    audits = MultiChoiceVar(choices=get_choices, label="Select Audit Classes", required=False)

    def run(self, data, commit):
        """Run the validate function on all given AuditRuleset classes."""
        audits = data.get("audits")

        audit_classes = []
        for registry_classes in registry["plugin_audit_rulesets"].values():
            audit_classes.extend(registry_classes)

        for repo in GitRepository.objects.all():
            if "nautobot_data_validation_engine.audit_rulesets" in repo.provided_contents:
                module = import_python_file_from_git_repo(repo)
                if hasattr(module, "audit_rulesets"):
                    audit_classes.extend(module.audit_rulesets)
        for audit_class in audit_classes:
            if audits and audit_class.__name__ not in audits:
                continue
            ins = audit_class()
            self.log_info(f"Running {audit_class.__name__}")
            ins.audit(self)


jobs = [RunRegisteredAuditRulesets]
