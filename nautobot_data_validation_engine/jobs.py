"""Jobs for nautobot_data_validation_engine."""

from django.apps import apps as global_apps

from nautobot.extras.models import GitRepository
from nautobot.extras.jobs import Job, MultiChoiceVar, BooleanVar

from nautobot_data_validation_engine.custom_validators import get_data_compliance_rules_map, get_classes_from_git_repo


def get_data_compliance_rules():
    """Generate a list of Audit Ruleset classes that exist from the registry."""
    validators = []
    for rule_sets in get_data_compliance_rules_map().values():
        validators.extend(rule_sets)
    return validators


def get_choices():
    """Get choices from registry."""
    choices = []
    for ruleset_class in get_data_compliance_rules():
        choices.append((ruleset_class.__name__, ruleset_class.__name__))
    for repo in GitRepository.objects.all():
        if "nautobot_data_validation_engine.data_compliance_rules" in repo.provided_contents:
            for compliance_class in get_classes_from_git_repo(repo):
                choices.append((compliance_class.__name__, compliance_class.__name__))

    choices.sort()
    return choices


class RunRegisteredDataComplianceRules(Job):
    """Run the validate function on all registered DataComplianceRule classes."""

    selected_data_compliance_rules = MultiChoiceVar(
        choices=get_choices,
        label="Select Data Compliance Rules",
        required=False,
        description="Not selecting any rules will run all rules listed.",
    )
    override_enforce = BooleanVar(
        default=True,
        label="Override Ruleset Enforce",
        description="Override any enforce values set on the DataComplianceRule classes. Not overriding this value will cause any enforced ComplianceErrors to fail the job.",
    )

    def run(self, data, commit):
        """Run the validate function on all given DataComplianceRule classes."""
        selected_data_compliance_rules = data.get("selected_data_compliance_rules")
        override_enforce = data.get("override_enforce")

        compliance_classes = []
        compliance_classes.extend(get_data_compliance_rules())

        for repo in GitRepository.objects.all():
            if "nautobot_data_validation_engine.data_compliance_rules" in repo.provided_contents:
                compliance_classes.extend(get_classes_from_git_repo(repo))

        for compliance_class in compliance_classes:
            if selected_data_compliance_rules and compliance_class.__name__ not in selected_data_compliance_rules:
                continue
            self.log_info(f"Running {compliance_class.__name__}")
            app_label, model = compliance_class.model.split(".")
            for obj in global_apps.get_model(app_label, model).objects.all():
                ins = compliance_class(obj)
                if override_enforce:
                    ins.enforce = False
                ins.clean()


jobs = [RunRegisteredDataComplianceRules]
