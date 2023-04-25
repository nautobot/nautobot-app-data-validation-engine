# Audit Ruleset Guide

## AuditRuleset Class

The `AuditRuleset` class takes advantage of the `CustomValidator` workflow.  The basic idea is that during an object's `full_clean` method call, any `AuditRuleset` classes are called to run their `clean` method.  That method calls the class's `audit` method, which you should implement.  The expected return of the `audit` method is `None`; however, any issues found during the `audit` method should raise an `AuditError`.  Multiple key value pairs can be passed in to an `AuditError` to create multiple audit results.  If there are no `AuditErrors` that are raised, any existing audit results for the class will be marked as valid.  Otherwise, attributes that were passed in via an `AuditError` will be marked as invalid with the given message.

Any `AuditRuleset` class can have a `class_name` defined to provide a friendly name to be shown within in the UI.  The `enforce` variable can also be set to decide whether or not the `AuditError` caught in the `audit` method is raised again to the `clean` method, acting like a `ValidationError` wherever the original `full_clean` was called.

### Writing Audit Rulesets in a Plugin

To write an audit ruleset in a custom plugin, the plugin will need a `custom_validators.py` file.  Any classes that implement `AuditRuleset` should be listed in a `custom_validators` variable found within that file.

### Writing Audit Rulesets in a Remote Git Repository

A Git repository can be configured to add the `audit rulesets` context to store `AuditRuleset` classes in source control.  The plugin looks for a file called `custom_validators.py`, and will import any classes listed within a `custom_validators` variable there.  The Git repo sync job will highlight all classes that it finds and imports.

```python
### your_plugin/custom_validators.py

from nautobot_data_validation_engine.audit_rulesets import AuditRuleset, AuditError

class DeviceAuditRuleset(AuditRuleset):
    model = "dcim.device"

    def audit_one_name(self):
        # your logic to determine if this function has succeeded or failed
        if self.context["object"].name == "ams01-dist-01":
            raise AuditError({"name": "ams01-dist-01 was changed to ams-rt01"})
    
    def audit_region_set(self):
        if not self.context["object"].region:
            raise AuditError({"region": "Device should have a region set."})
    
    def audit(self):
        messages = {}
        for fn in [self.audit_one_name, self.audit_region_set]:
            try:
                fn()
            except AuditError as ex:
                messages.update(ex.message_dict)
        if messages:
            raise AuditError(messages)
        

audit_rulesets = [DeviceAuditRuleset]

```

The job provided in the `jobs.py` file can be run via the UI to the `clean` method on any `AuditRuleset` class available to the plugin.

## Viewing Results

All audit rules can be found on the navigation bar under `Extensibility -> Data Validation Engine -> Audit Results`. This is a basic table that lists all records in the table currently.

The `nautobot_data_validation_engine` app automatically creates template extensions to add a `Audits` tab to the detail view of all objects.  The `Audits` tab will only be visible if there is an `Audit` that exists for that model.