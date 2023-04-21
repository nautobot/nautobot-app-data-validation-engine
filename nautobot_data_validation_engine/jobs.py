"""Jobs for nautobot_data_validation_engine."""

from django.apps import apps as global_apps

# from django.contrib.auth import get_user_model
# from django.core.exceptions import ValidationError
from nautobot.extras.models import GitRepository
from nautobot.extras.jobs import Job, MultiChoiceVar  # , BooleanVar

from .custom_validators import get_audit_rule_sets  # , get_audit_rule_sets_map
from .utils import import_python_file_from_git_repo


def get_choices():
    """Get choices from registry."""
    choices = []
    for ruleset_class in get_audit_rule_sets():
        choices.append((ruleset_class.__name__, ruleset_class.__name__))
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
        audit_classes.extend(get_audit_rule_sets())

        for repo in GitRepository.objects.all():
            if "nautobot_data_validation_engine.audit_rulesets" in repo.provided_contents:
                module = import_python_file_from_git_repo(repo)
                if hasattr(module, "audit_rulesets"):
                    audit_classes.extend(module.audit_rulesets)

        for audit_class in audit_classes:
            if audits and audit_class.__name__ not in audits:
                continue
            self.log_info(f"Running {audit_class.__name__}")
            app_label, model = audit_class.model.split(".")
            for obj in global_apps.get_model(app_label, model).objects.all():
                ins = audit_class(obj)
                ins.clean()


# class AuditAllObjects(Job):
#     """Job to audit all models that currently have existing validations."""

#     full_clean = BooleanVar(label="Full Clean", description="Run all validations in addition to audit rules")

#     def run(self, data, commit=False):
#         """Audit all models."""
#         full_clean: bool = data["full_clean"]
#         auditor_classes = get_audit_rule_sets_map()
#         for app_config in sorted(list(global_apps.get_app_configs()), key=lambda x: x.label):
#             for model in sorted(list(app_config.models.values()), key=lambda x: x._meta.model_name):
#                 model_name = f"{model._meta.app_label}.{model._meta.model_name}"
#                 # Must swap out for user_model
#                 if model_name == "auth.user":
#                     model = get_user_model()
#                 # Skip models that aren't actually in the database
#                 if not model._meta.managed:
#                     continue
#                 self.job_result.log_info(f" --> {type(self).__name__} is Validating Model: {model_name}")

#                 model.objects.all()
#                 for instance in model.objects.all().iterator():
#                     if full_clean:
#                         try:
#                             instance.full_clean()
#                         except ValidationError as err:
#                             for attribute, messages in err.message_dict.items():
#                                 self.fail(
#                                     instance,
#                                     attribute=attribute,
#                                     validated_attribute_value=getattr(instance, attribute),
#                                     message=" AND ".join(messages),
#                                 )

#                     for auditor_class in auditor_classes.get(model_name, []):
#                         auditor = auditor_class(model)
#                         auditor.audit()


jobs = [RunRegisteredAuditRulesets]
