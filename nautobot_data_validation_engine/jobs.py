"""Jobs for nautobot_data_validation_engine."""
from nautobot.extras.jobs import Job, MultiChoiceVar
from nautobot.extras.utils import registry


def get_choices():
    """Get choices from registry."""
    choices = []
    for classes in registry["plugin_audit_rulesets"].values():
        for audit_class in classes:
            choices.append((audit_class.__name__, audit_class.__name__))
    choices.sort()
    return choices


class RunRegisteredAuditRulesets(Job):
    """Run the validate function on all registered AuditRuleset classes."""

    audits = MultiChoiceVar(choices=get_choices, label="Select Audit Classes", required=False)

    def run(self, data, commit):
        """Run the validate function on all given AuditRuleset classes."""
        audits = data.get("audits")

        for classes in registry["plugin_audit_rulesets"].values():
            for audit_class in classes:
                if audits and audit_class.__name__ not in audits:
                    continue
                ins = audit_class()
                self.log_info(f"Running {audit_class.__name__}")
                ins.audit(self)


jobs = [RunRegisteredAuditRulesets]
