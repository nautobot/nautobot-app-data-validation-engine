# Data Compliance Guide

## DataComplianceRule Class

The `DataComplianceRule` class takes advantage of the `CustomValidator` workflow.  The basic idea is that during an object's `full_clean` method call, any `DataComplianceRule` classes are called to run their `clean` method.  That method calls the class's `audit` method, which you should implement.  The expected return of the `audit` method is `None`; however, any issues found during the `audit` method should raise an `ComplianceError`.  Multiple key value pairs can be passed in to an `ComplianceError`.  The data within a `ComplianceError` is used by the `clean` method to create `DataCompliance` objects, which relates the given object to the `DataComplianceRule` class, the attribute checked, and the message passed into the `ComplianceError` as to why the attribute is not valid.  If there are no `ComplianceErrors` raised within the `audit` method, any existing `DataCompliance` objects for the given object and `DataComplianceRule` pair are marked as valid.

`DataCompliance` objects are only created for `__all__` (to represent an overall status) and attributes that have at some point been invalid.  As an example, suppose there is a `DataComplianceRule` that checks the `foo` and `bar` attributes of an object.  When this rule is run for object A, both attributes are valid, so the only `DataCompliance` object created would be for `__all__`.  Then, object A's `foo` attribute is edited in a way that makes it invalid.  A new `DataCompliance` object would be created for `foo` stating why it is invalid, and the `__all__` object would be updated to now be invalid.  Then, if `foo` is edited again to bring it back into compliance, the `DataCompliance` objects for `foo` and `__all__` would be updated to be valid.

Any `DataComplianceRule` class can have a `name` defined to provide a friendly name to be shown within in the UI.  The `enforce` attribute can also be set to decide whether or not the `ComplianceError` caught in the `audit` method is raised again to the `clean` method, acting like a `ValidationError` wherever the original `full_clean` was called.  Setting `enforce` to `True` changes the `DataComplianceRule` from a passive validation of data to an active enforcement of the logic within it.

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

The provided `RunRegisteredDataComplianceRules` job can be used to run the `audit` method for any number of registered `DataComplianceRule` classes in an ad-hoc fashion.  This can be used to rerun the data compliance rules for the first time over a set of objects or rerun the rules after an update to the compliance logic.

## Viewing Results

All data compliance objects can be found on the navigation bar under `Extensibility -> Data Validation Engine -> Data Compliance`. This view lists all available data compliance results.

The `nautobot_data_validation_engine` app automatically creates template extensions to add a `Data Compliance` tab to the detail view of all objects.