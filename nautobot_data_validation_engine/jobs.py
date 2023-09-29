"""Jobs for nautobot_data_validation_engine."""

from django.apps import apps as global_apps

from nautobot.core.celery import register_jobs
from nautobot.extras.models import GitRepository
from nautobot.extras.jobs import Job, MultiChoiceVar, get_task_logger

from nautobot_data_validation_engine.custom_validators import get_data_compliance_rules_map, get_classes_from_git_repo
from nautobot_data_validation_engine.models import DataCompliance

logger = get_task_logger(__name__)


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

    name = "Run Registered Data Compliance Rules"
    description = "Runs selected Data Compliance rule classes."

    selected_data_compliance_rules = MultiChoiceVar(
        choices=get_choices,
        label="Select Data Compliance Rules",
        required=False,
        description="Not selecting any rules will run all rules listed.",
    )

    def run(self, *args, **kwargs):
        """Run the validate function on all given DataComplianceRule classes."""
        selected_data_compliance_rules = kwargs.get("selected_data_compliance_rules", None)

        compliance_classes = []
        compliance_classes.extend(get_data_compliance_rules())

        for repo in GitRepository.objects.all():
            if "nautobot_data_validation_engine.data_compliance_rules" in repo.provided_contents:
                compliance_classes.extend(get_classes_from_git_repo(repo))

        for compliance_class in compliance_classes:
            if selected_data_compliance_rules and compliance_class.__name__ not in selected_data_compliance_rules:
                continue
            logger.info(f"Running {compliance_class.__name__}")
            app_label, model = compliance_class.model.split(".")
            for obj in global_apps.get_model(app_label, model).objects.all():
                ins = compliance_class(obj)
                ins.enforce = False
                ins.clean()


class DeleteOrphanedDataComplianceData(Job):
    """Utility job to delete any Data Compliance objects where the validated object no longer exists."""

    name = "Delete Orphaned Data Compliance Data"
    description = "Delete any Data Compliance objects where its validated object no longer exists."

    def run(self, *args, **kwargs):
        """Delete DataCompliance objects where its validated_object no longer exists."""
        number_deleted = 0
        for obj in DataCompliance.objects.all():
            if obj.validated_object is None:
                logger.info(f"Deleting {obj}.")
                obj.delete()
                number_deleted += 1
        logger.info(f"Deleted {number_deleted} orphaned DataCompliance objects.")


jobs = (
    RunRegisteredDataComplianceRules,
    DeleteOrphanedDataComplianceData,
)
register_jobs(*jobs)
