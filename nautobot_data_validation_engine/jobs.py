"""Jobs for nautobot_data_validation_engine."""

from django.apps import apps as global_apps
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from nautobot.core.celery import register_jobs
from nautobot.extras.models import GitRepository
from nautobot.extras.jobs import Job, MultiChoiceVar, get_task_logger, BooleanVar
from nautobot.extras.plugins import CustomValidator, ValidationError
from nautobot.extras.registry import registry

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

    run_existing_rules_in_report = BooleanVar(
        label="Run existing validation rules", description="Include manually created data validation rules in report?"
    )

    def run(self, run_existing_rules_in_report, *args, **kwargs):
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

        if run_existing_rules_in_report:
            self.report_for_validation_rules()

    @staticmethod
    def report_for_validation_rules():
        """Run existing data validation rules and add to report."""
        query = (
            Q(uniquevalidationrule__isnull=False)
            | Q(regularexpressionvalidationrule__isnull=False)
            | Q(minmaxvalidationrule__isnull=False)
            | Q(requiredvalidationrule__isnull=False)
        )

        model_classes = [ct.model_class() for ct in ContentType.objects.filter(query).distinct()]

        # Gather custom validators of existing rules
        validator_dicts = []
        for model_class in model_classes:
            model_custom_validators = registry["plugin_custom_validators"][model_class._meta.label_lower]
            # Get only DataValidationCustomValidators
            # otherwise, we would get all validators (more than those dynamically created)
            validator_dicts.extend(
                [
                    {cv: model_class}
                    for cv in model_custom_validators
                    if cv.__name__
                    == f"{model_class._meta.app_label.capitalize()}{model_class._meta.model_name.capitalize()}CustomValidator"
                ]
            )

        # Run validation on exisiting objects and add to report
        for validator_dict in validator_dicts:
            for validator, class_name in validator_dict.items():
                if getattr(validator, "clean") == getattr(CustomValidator, "clean"):
                    continue

                for validated_object in class_name.objects.all():
                    try:
                        validator(validated_object).clean(exclude_disabled_rules=False)
                        validator.compliance_result(
                            validator,
                            instance=validated_object,
                            valid=True,
                        )
                    except ValidationError as error:
                        validator.compliance_result(
                            validator,
                            instance=validated_object,
                            message=error.messages[0],
                            attribute=list(error.message_dict.keys())[0],
                            valid=False,
                        )


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
