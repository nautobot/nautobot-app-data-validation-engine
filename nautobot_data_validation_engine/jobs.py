from nautobot.extras.jobs import Job, MultiChoiceVar
from nautobot.extras.utils import registry
from nautobot_data_validation_engine import CHOICES


class RunRegisteredValidations(Job):
    validators = MultiChoiceVar(choices=CHOICES, label="Select Validator", required=False)

    def run(self, data, commit):
        validators = data.get("validators")

        for model, classes in registry["plugin_validations"].items():
            for validation_class in classes:
                if validators and validation_class.__name__ not in validators:
                    continue
                ins = validation_class()
                self.log_info(f"Running {type(ins).__name__}")
                ins.validate(self)


jobs = [RunRegisteredValidations]
