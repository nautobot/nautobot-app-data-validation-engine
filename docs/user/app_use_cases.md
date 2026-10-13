# Using the App

This document describes common use-cases and scenarios for this App.

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
* content type - The Nautobot model to which the rule should apply (e.g. device, location, etc.).
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
* content type - The Nautobot model to which the rule should apply (e.g. device, location, etc.).
* field - The name of the character based field on the model to which the regular expression is validated.
* regular expression - The body of the regular expression used for validation.
* context processing - A boolean to toggle Jinja2 context processing of the regular expression prior to evaluation. See the warnings below for how interpolated values are treated.
* error message - An optional error message to display to the use when validation fails. By default, a message indicating validation against the defined regular expression has failed is shown.

![Regex Rules Edit](../images/regex-rules-edit.png)

In this example, a device hostname validation rule has been created and prevents device records from being created or updated that do not conform to the naming standard.

![Regex Rules Enforcement](../images/regex-rules-enforcement.png)

Regex rules may also support complex Jinja2 rendering called context processing which allows for the regular expression itself to by dynamically generated based on the context of the data it is validating.

In this example the name of a device must start with the first three characters of the name of the location to which the device belongs. The dynamic nature of the Jinja2 rendering means that the location name can be anything, the enforcement action is simply that the given device name matches its assigned location.

![Regex Rules Jinja2 Context Processing](../images/regex-rules-jinja2-context-processing.png)

!!! warning
    If there is an exception while rendering the Jinja2 template or the resulting regular expression string is invalid, data validation against the rule will fail and users will be instructed to either fix the rule or disable it before the data may be saved.

+/- 3.4.1 "Interpolated values are now treated as literal text"
    Values interpolated with `{{ ... }}` are escaped before the pattern is compiled, so any regular expression metacharacter they contain matches literally. This keeps the structure of the pattern entirely under the rule author's control, so that the data being validated cannot change what the rule means. Literal text written in the rule itself is untouched, so the author's own regular expression syntax works as normal.

    There are two important effects to keep in mind. First, an expression like `[{{ object.name }}]` no longer lets the field value supply character-class syntax such as a range. The brackets you wrote are still a character class, but every metacharacter in the interpolated value is escaped, so it contributes only literal members. For example, if the object's name is `A-Z` and the rule is `[{{ object.name }}]`, the rendered expression will be `[A\-Z]` (matching only `A`, `-`, or `Z`) rather than `[A-Z]` (matching any character from `A` through `Z`). Second, if a field value is itself a piece of regular expression syntax, it will be treated as plain text and not as part of the regex pattern. This behavior is always enforced and cannot be disabled. Additionally, do not use `{% set %}...{% endset %}` capture blocks, as their contents will be escaped twice; instead, use simple assignments such as `{% set x = object.name %}`.

+/- 3.4.1 "Regular expression evaluation is now time-bounded"
    Each rule is evaluated every time an object of the targeted type is saved, so an expensive expression slows down every such save. Evaluation is bounded to one second per rule per object, configurable via Nautobot's `REGEX_TIMEOUT` setting (Nautobot v2.4.44 and later); if that limit is exceeded the save is rejected with a validation error and the responsible rule is named in the server log at `ERROR` level.

    Some regular expressions take exponentially longer to evaluate as the value being tested grows, which means an expression that looks harmless can be made to consume that full second by a sufficiently long value. The usual causes are a quantifier applied to a group that itself contains a quantifier, and alternations whose branches can match the same input. Note that the data compliance audit job evaluates disabled rules as well as enabled ones, so a costly rule still has a cost after being disabled.

### Required Rules

![Required List](../images/required-rules-list.png)

Each rule is defined with these fields:

* name - A unique name for the rule.
* enabled - A boolean to toggle enforcement of the rule on and off.
* content type - The Nautobot model to which the rule should apply (e.g. device, location, etc.).
* field - The name of the field on the Nautobot model which should always be required.
* error message - An optional error message to display to the user when validation fails. By default, a message indicating the field may not be left blank is shown.

![Required Rules Edit](../images/required-rules-edit.png)

In this example, a rule is enforcing that location objects must always have a description populated.

![Required Rules Enforcement](../images/required-rules-enforcement.png)

### Unique Rules

![Unique List](../images/unique-rules-list.png)

Each rule is defined with these fields:

* name - A unique name for the rule.
* enabled - A boolean to toggle enforcement of the rule on and off.
* content type - The Nautobot model to which the rule should apply (e.g. device, location, etc.).
* field - The name of the field on the Nautobot model which should always be required.
* max instances - The total number of records that may have the same unique value for the given field. Default of 1.
* error message - An optional error message to display to the user when validation fails. By default, a message indicating the value already exists on another record or set of records, as determined by max instances.

![Unique Rules Edit](../images/unique-rules-edit.png)

In this example, the rule enforces that the assigned ASN for a location is unique across all other locations.

![Unique Rules Enforcement](../images/unique-rules-enforcement.png)
