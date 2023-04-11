"""Jobs for nautobot_data_validation_engine."""
from nautobot.extras.jobs import Job, MultiChoiceVar
from nautobot.extras.utils import registry
from nautobot_data_validation_engine import CHOICES


class RunRegisteredValidations(Job):
    """Run the validate function on all registered ValidationSet classes."""

    validators = MultiChoiceVar(choices=CHOICES, label="Select Validator", required=False)

    def run(self, data, commit):
        """Run the validate function on all given ValidationSet classes."""
        validators = data.get("validators")

        for classes in registry["plugin_validations"].values():
            for validation_class in classes:
                if validators and validation_class.__name__ not in validators:
                    continue
                ins = validation_class()
                self.log_info(f"Running {type(ins).__name__}")
                ins.validate(self)


jobs = [RunRegisteredValidations]