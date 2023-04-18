"""Jobs for nautobot_data_validation_engine."""
from django.apps import apps as global_apps
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from nautobot.extras.jobs import Job, MultiChoiceVar, BooleanVar

from .audit_rulesets import get_audit_rule_sets, get_audit_rule_sets_map


def get_choices():
    """Get choices from registry."""
    choices = []
    for ruleset_class in get_audit_rule_sets():
        choices.append((ruleset_class.__name__, ruleset_class.__name__))
    choices.sort()
    return choices


class RunRegisteredAuditRulesets(Job):
    """Run the validate function on all registered AuditRuleset classes."""

    audits = MultiChoiceVar(choices=get_choices, label="Select Audit Classes", required=False)

    def run(self, data, commit):
        """Run the validate function on all given AuditRuleset classes."""
        audits = data.get("audits")
        for rule_set in get_audit_rule_sets():
            if rule_set.__name__ == audits:
                ins = rule_set()
                self.log_info(f"Running {rule_set.__name__}")
                ins.audit(self)


class AuditAllObjects(Job):
    full_clean = BooleanVar(label="Full Clean", description="Run all validations in addition to audit rules")

    def run(self, data, commit=False):
        full_clean: bool = data["full_clean"]
        auditor_classes = get_audit_rule_sets_map()
        for app_config in sorted(list(global_apps.get_app_configs()), key=lambda x: x.label):
            for model in sorted(list(app_config.models.values()), key=lambda x: x._meta.model_name):
                model_name = f"{model._meta.app_label}.{model._meta.model_name}"
                # Must swap out for user_model
                if model_name == "auth.user":
                    model = get_user_model()
                # Skip models that aren't actually in the database
                if not model._meta.managed:
                    continue
                self.job_result.log_info(f" --> {type(self).__name__} is Validating Model: {model_name}")

                model.objects.all()
                for instance in model.objects.all().iterator():
                    if full_clean:
                        try:
                            instance.full_clean()
                        except ValidationError as err:
                            for attribute, messages in err.message_dict.items():
                                self.fail(
                                    instance,
                                    attribute=attribute,
                                    validated_attribute_value=getattr(instance, attribute),
                                    message=" AND ".join(messages),
                                )

                    for auditor_class in auditor_classes.get(model_name, []):
                        auditor = auditor_class(model)
                        auditor.audit()


jobs = [RunRegisteredAuditRulesets]
