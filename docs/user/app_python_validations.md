# Python Data Validation Guide

## Writing Validations

To write validation methods for your plugin, create a `validations.py` file within your plugin. Each class within this file should inherit from the `AuditRuleset` class from `nautobot_data_validation_engine.validations`. The `AuditRuleset` class provides `success` and `fail` methods to create `AuditRule` objects. Additionally, the name of any validation methods written in your implementations must start with `validate_` to be considered a validation. The `validate_` functions takes an parameter `instance` which is the instance of the given model you wish to validate.

```python
### your_plugin/validations.py

from nautobot_data_validation_engine.validations import AuditRuleset
from nautobot.dcim.models import Device

class DeviceAuditRuleset(AuditRuleset):
    model = "dcim.device"

    def get_queryset(self):
        # optional: used to override the default queryset
        # default queryset is all objects of the given model
        return Device.objects.all()

    def validate_one_name(self, instance):
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

validations = [DeviceAuditRuleset]

```

The job provided in the `jobs.py` file can be run via the UI to run all validate methods across all validation classes added to the `validations` variable.

## Viewing Results

All validation results can be found on the navigation bar under `Extensibility -> Data Validation Engine -> Pythonic Validations`. This is a basic table that lists all records in the table currently.

The `nautobot_data_validation_engine` app automatically creates template extensions to add a `Validations` tab to the detail view of all objects.  The visibility of this tab can be set via the `VALIDATION_TAB_VISIBILITY` configuration in `PLUGINS_CONFIG`.
* Setting `ALWAYS` (the default) will show the `Validations` tab regardless of `AuditRule` records.
* Setting `MODEL` will only show the `Validations` tab if there is a `AuditRule` that matches the content type of the object.
* * For example, all `dcim.site` objects will have a `Validations` tab if there is at least one `AuditRule` with `dcim.site` as its content type.
* Setting `INSTANCE` will only show the `Validations` tab if there is at least one `AuditRule` for the specific object.
* * For example, while viewing a specific `Site` object, the `Validations` tab will only be visible if there is at least one `AuditRule` related to it.