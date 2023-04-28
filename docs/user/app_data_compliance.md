# Data Compliance Guide

## DataComplianceRule Class

The `DataComplianceRule` class takes advantage of the `CustomValidator` workflow.  The basic idea is that during an object's `full_clean` method call, any `DataComplianceRule` classes are called to run their `clean` method.  That method calls the class's `audit` method, which you should implement.  The expected return of the `audit` method is `None`; however, any issues found during the `audit` method should raise an `ComplianceError`.  Multiple key value pairs can be passed in to an `ComplianceError` to create multiple data compliance objects.  If there are no `AuditErrors` that are raised, any existing data compliance objects for the class will be marked as valid.  Otherwise, attributes that were passed in via an `ComplianceError` will be marked as invalid with the given message.

Any `DataComplianceRule` class can have a `class_name` defined to provide a friendly name to be shown within in the UI.  The `enforce` variable can also be set to decide whether or not the `ComplianceError` caught in the `audit` method is raised again to the `clean` method, acting like a `ValidationError` wherever the original `full_clean` was called.

### Writing Data Compliance Rules in a Plugin

To write a data compliance rule in a custom plugin, the plugin will need a `custom_validators.py` file.  Any classes that implement `DataComplianceRule` should be listed in a `custom_validators` variable found within that file.

### Writing Data Compliance Rules in a Remote Git Repository

A Git repository can be configured to add the `data compliance rules` context to store `DataComplianceRule` classes in source control.  The plugin looks for a folder called `custom_validators`, and any classes that implement `DataComplianceRule` within any file in that folder will be imported.  There is no need to list the classes in any variable.  The Git repo sync job will highlight all classes that it finds and imports.

```python
### your_plugin/custom_validators.py

from nautobot_data_validation_engine.custom_validators import DataComplianceRule, ComplianceError

class DeviceDataComplianceRule(DataComplianceRule):
    model = "dcim.device"

    def audit_one_name(self):
        # your logic to determine if this function has succeeded or failed
        if self.context["object"].name == "ams01-dist-01":
            raise ComplianceError({"name": "ams01-dist-01 was changed to ams-rt01"})
    
    def audit_region_set(self):
        if not self.context["object"].region:
            raise ComplianceError({"region": "Device should have a region set."})
    
    def audit(self):
        messages = {}
        for fn in [self.audit_one_name, self.audit_region_set]:
            try:
                fn()
            except ComplianceError as ex:
                messages.update(ex.message_dict)
        if messages:
            raise ComplianceError(messages)
        

custom_validators = [DeviceDataComplianceRule]

```

The job provided in the `jobs.py` file can be run via the UI to the `clean` method on any `DataComplianceRule` class available to the plugin.

## Viewing Results

All data compliance objects can be found on the navigation bar under `Extensibility -> Data Validation Engine -> Data Compliance`. This is a basic table that lists all records in the table currently.

The `nautobot_data_validation_engine` app automatically creates template extensions to add a `Data Compliance` tab to the detail view of all objects.  The `Data Compliance` tab will only be visible if there is an `DataCompliance` object that exists for that model.