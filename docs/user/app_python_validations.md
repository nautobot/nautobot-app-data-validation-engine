# Python Data Validation Guide

## Writing Validations

To write validation methods for your plugin, create a `validations.py` file within your plugin. Each class within this file should inherit from the `ValidationSet` class from `nautobot_data_validation_engine.validations`. The `ValidationSet` class provides `success` and `fail` methods to create `ValidationResult` objects. Additionally, the name of any validation methods written in your implementations must start with `validate_` to be considered a validation. The `validate_` functions takes an parameter `instance` which is the instance of the given model you wish to validate.

```python
### your_plugin/validations.py

from nautobot_data_validation_engine.validations import ValidationSet
from nautobot.dcim.models import Device

class DeviceValidationSet(ValidationSet):
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

validations = [DeviceValidationSet]

```

The job provided in the `jobs.py` file can be run via the UI to run all validate methods across all validation classes added to the `validations` variable.

## Viewing Results

All validation results can be found on the navigation bar under `Extensibility -> Data Validation Engine -> Pythonic Validations`. This is a basic table that lists all records in the table currently.

The `ObjectValidationView` class can be implemented in your plugin to display all results related to a specific validated object. This class will create an additional detail tab on the object's detail view page.

```python
### your_plugin/views.py
from nautobot_data_validation_engine.views import ObjectValidationview
from your_plugin.models import ModelA

class ModelAValidationView(ObjectValidationView):
    queryset = ModelA.objects.all()
```

```python
### your_plugin/urls.py
...
from django.urls import path
from your_plugin import views
...

urlpatterns = [
    ...
    path("model_a/<id>", views.ModelAValidationView.as_view(), name="modela_validation"),
    ...
]
```

```python
### your_plugin/template_content.py
from nautobot_data_validation_engine.template_content import ValidationTab

class ModelAValidationTab(ValidationTab):
    model = "your_plugin.modela"
    view_name = "plugins:your_model:modela_validation"

...

template_extensions = [ModelAValidationTab]
```