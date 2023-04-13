# Audit Ruleset Guide

## Writing Audit Rules

To write audit methods for your plugin, create a `audit_rulesets.py` file within your plugin. Each class within this file should inherit from the `AuditRuleset` class from `nautobot_data_validation_engine.audit_rulesets`. The `AuditRuleset` class provides `success` and `fail` methods to create `AuditResult` objects. Additionally, the name of any audit methods written in your implementations must start with `audit_` to be considered a audit rule. The `audit_` functions takes an parameter `instance` which is the instance of the given model you wish to audit.

```python
### your_plugin/validations.py

from nautobot_data_validation_engine.audit_rulesets import AuditRuleset
from nautobot.dcim.models import Device

class DeviceAuditRuleset(AuditRuleset):
    model = "dcim.device"

    def get_queryset(self):
        # optional: used to override the default queryset
        # default queryset is all objects of the given model
        return Device.objects.all()

    def audit_one_name(self, instance):
        # your logic to determine if this function has succeeded or failed
        if instance.name == "ams01-dist-01":
            self.fail(
                instance,
                attribute="name",
                validated_attribute_value=instance.name,
                message="ams01-dist-01 was changed to ams-rt01",
                expected_attribute_value="ams-rt01",
            )
        else:
            self.success(instance, attribute="name", validated_attribute_value=instance.name)

audit_rulesets = [DeviceAuditRuleset]

```

The job provided in the `jobs.py` file can be run via the UI to run all audit methods across all `AuditRuleset` classes added to the `audit_rulesets` variable.

## Viewing Results

All audit rules can be found on the navigation bar under `Extensibility -> Data Validation Engine -> Audit Results`. This is a basic table that lists all records in the table currently.

The `nautobot_data_validation_engine` app automatically creates template extensions to add a `Audit Results` tab to the detail view of all objects.  The `Audit Results` tab will only be visible if there is an `AuditResult` that exists for that model.