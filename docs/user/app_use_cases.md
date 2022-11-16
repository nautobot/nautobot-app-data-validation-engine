# Using the App

## General Usage

The data validation engine app offers a set of user definable rules which are used to enforce business constraints on the data in Nautobot. These rules are tied to particular models and each rule is meant to enforce one aspect of a business use case.

Supported rule types include:
- Regular expression
- Min/max value
- Required fields
- Unique values

![Dropdown](../images/dropdown.png)

## Use-cases and common workflows

### Min/Max Rules

![Min/Max Rules List](../images/min-max-rules-list.png)

Each rule is defined with these fields:

* name - A unique name for the rule.
* enabled - A boolean to toggle enforcement of the rule on and off.
* content type - The Nautobot model to which the rule should apply (device, site, etc.).
* field - The name of the numeric based field on the model to which the min/max value is validated.
* min - The min value to validate value against (greater than or equal).
* max - The max value to validate value against (less than or equal).
* error message - An optional error message to display to the user when validation fails. By default, a message indicating validation against the defined min/max value has failed is shown.

![Min/Max Rules Edit](../images/min-max-rules-edit.png)

In this example, a max value for VLAN IDs has been configured, preventing VLANs greater than 3999 from being created.

![Min/Max Rules Enforcement](../images/min-max-rules-enforcement.png)

### Regular Expression Rules

![Regex Rules List](../images/regex-rules-list.png)

Each rule is defined with these fields:

* name - A unique name for the rule.
* enabled - A boolean to toggle enforcement of the rule on and off.
* content type - The Nautobot model to which the rule should apply (device, site, etc.).
* field - The name of the character based field on the model to which the regular expression is validated.
* regular expression - The body of the regular expression used for validation.
* context processing - A boolean to toggle Jinja2 context processing of the regular expression prior to evaluation
* error message - An optional error message to display to the use when validation fails. By default, a message indicating validation against the defined regular expression has failed is shown.

![Regex Rules Edit](../images/regex-rules-edit.png)

In this example, a device hostname validation rule has been created and prevents device records from being created or updated that do not conform to the naming standard.

![Regex Rules Enforcement](../images/regex-rules-enforcement.png)

Regex rules may also support complex Jinja2 rendering called context processing which allows for the regular expression itself to by dynamically generated based on the context of the data it is validating.

In this example the name of a device must start with the first three characters of the name of the site to which the device belongs. The dynamic nature of the Jinja2 rendering means that the site name can be anything, the enforcement action is simply the the given device matches its assigned site.

![Regex Rules Jinja2 Context Processing](../images/regex-rules-jinja2-context-processing.png)

!!! warning
    If there is an exception while rendering the Jinja2 template or the resulting regular expression string is invalid, data validation against the rule will fail and users will be instructed to either fix the rule or disable it before the data may be saved.

### Required Rules

![Required List](../images/required-rules-list.png)

Each rule is defined with these fields:

* name - A unique name for the rule.
* enabled - A boolean to toggle enforcement of the rule on and off.
* content type - The Nautobot model to which the rule should apply (device, site, etc.).
* field - The name of the field on the Nautobot model which should always be required.
* error message - An optional error message to display to the user when validation fails. By default, a message indicating the field may not be left blank is shown.

![Required Rules Edit](../images/required-rules-edit.png)

In this example, a rule is enforcing that site objects must always have a description populated.

![Required Rules Enforcement](../images/required-rules-enforcement.png)

### Unique Rules

![Unique List](../images/required-rules-list.png)

Each rule is defined with these fields:

* name - A unique name for the rule.
* enabled - A boolean to toggle enforcement of the rule on and off.
* content type - The Nautobot model to which the rule should apply (device, site, etc.).
* field - The name of the field on the Nautobot model which should always be required.
* max instances - The total number of records that may have the same unique value for the given field. Default of 1.
* error message - An optional error message to display to the user when validation fails. By default, a message indicating the value already exists on another record or set of records, as determined by max instances.

![Unique Rules Edit](../images/required-rules-edit.png)

In this example, sites enforce that the assigned ASN is unique across all other sites.

![Unique Rules Enforcement](../images/required-rules-enforcement.png)