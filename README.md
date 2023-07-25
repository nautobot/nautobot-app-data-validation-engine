# Data Validation Engine

<p align="center">
  <img src="https://raw.githubusercontent.com/nautobot/nautobot-plugin-data-validation-engine/develop/docs/images/icon-DataValidationEngine.png" class="logo" height="200px">
  <br>
  <a href="https://github.com/nautobot/nautobot-plugin-data-validation-engine/actions"><img src="https://github.com/nautobot/nautobot-plugin-data-validation-engine/actions/workflows/ci.yml/badge.svg?branch=develop"></a>
  <a href="https://docs.nautobot.com/projects/data-validation/en/latest"><img src="https://readthedocs.org/projects/nautobot-plugin-data-validation-engine/badge/"></a>
  <a href="https://pypi.org/project/nautobot-data-validation-engine/"><img src="https://img.shields.io/pypi/v/nautobot-data-validation-engine"></a>
  <a href="https://pypi.org/project/nautobot-data-validation-engine/"><img src="https://img.shields.io/pypi/dm/nautobot-data-validation-engine"></a>
  <br>
  An App for <a href="https://github.com/nautobot/nautobot">Nautobot</a>.
</p>

## Overview

An app for [Nautobot](https://github.com/nautobot/nautobot) with a UI to build custom data validation rules for Source of Truth data.

The Data Validation Engine app offers a set of user definable rules which are used to enforce business constraints on the data in Nautobot. These rules are tied to particular models and each rule is meant to enforce one aspect of a business use case.

Supported rule types include:
- Regular expression
- Min/max value
- Required fields
- Unique values

Another feature within the app called [Data Compliance](https://docs.nautobot.com/projects/data-validation/en/latest/user/app_data_compliance/) can audit any object within Nautobot according to a set of rules that you can define programmatically. Unlike the other rule types within the Data Validation Engine app that only check for adherence to specified rules during the creation or modification of objects, Data Compliance will run a job that produces compliance statuses across all objects including pre-existing ones (such as all existing devices).

![Dropdown](https://raw.githubusercontent.com/nautobot/nautobot-plugin-data-validation-engine/develop/docs/images/dropdown.png)

### Screenshots

More screenshots can be found in the [Using the App](https://docs.nautobot.com/projects/data-validation/en/latest/user/app_use_cases/) page in the documentation. Here's a quick overview of some of the app's added functionality:

**Min/Max Rules**

![Min/Max List](https://raw.githubusercontent.com/nautobot/nautobot-plugin-data-validation-engine/develop/docs/images/min-max-rules-list.png)

**Regular Expression Rules**

![Regex Rules List](https://raw.githubusercontent.com/nautobot/nautobot-plugin-data-validation-engine/develop/docs/images/regex-rules-list.png)

**Required Rules**

![Required Rules List](https://raw.githubusercontent.com/nautobot/nautobot-plugin-data-validation-engine/develop/docs/images/required-rules-list.png)

**Unique Rules**

![Unique Rules List](https://raw.githubusercontent.com/nautobot/nautobot-plugin-data-validation-engine/develop/docs/images/unique-rules-list.png)

**Data Compliance**

![Data Compliance Results List](https://raw.githubusercontent.com/nautobot/nautobot-plugin-data-validation-engine/develop/docs/images/data-compliance-results-list.png)

## Try it out!

This App is installed in the Nautobot Community Sandbox found over at [demo.nautobot.com](https://demo.nautobot.com/)!

> For a full list of all the available always-on sandbox environments, head over to the main page on [networktocode.com](https://www.networktocode.com/nautobot/sandbox-environments/).

## Documentation

Full web-based HTML documentation for this app can be found over on the [Nautobot Docs](https://docs.nautobot.com) website:

- [User Guide](https://docs.nautobot.com/projects/data-validation/en/latest/user/app_overview/) - Overview, Getting Started, Using the App.
- [Administrator Guide](https://docs.nautobot.com/projects/data-validation/en/latest/admin/install/) - How to Install, Configure, Upgrade, or Uninstall the App.
- [Developer Guide](https://docs.nautobot.com/projects/data-validation/en/latest/dev/contributing/) - Extending the App, Code Reference, Contribution Guide.
- [Release Notes / Changelog](https://docs.nautobot.com/projects/data-validation/en/latest/admin/release_notes/).
- [Frequently Asked Questions](https://docs.nautobot.com/projects/data-validation/en/latest/user/faq/).

### Contributing to the Docs

You can find all the Markdown source for the App documentation under the [docs](https://github.com/nautobot/nautobot-plugin-data-validation-engine/tree/develop/docs) folder in this repository. For simple edits, a Markdown capable editor is sufficient - clone the repository and edit away.

If you need to view the fully generated documentation site, you can build it with [mkdocs](https://www.mkdocs.org/). A container hosting the docs will be started using the invoke commands (details in the [Development Environment Guide](https://docs.nautobot.com/projects/data-validation/en/latest/dev/dev_environment/#docker-development-environment)) on [http://localhost:8001](http://localhost:8001). As your changes are saved, the live docs will be automatically reloaded.

Any PRs with fixes or improvements are very welcome!

## Questions

For any questions or comments, please check the [FAQ](https://docs.nautobot.com/projects/data-validation/en/latest/user/faq/) first. Feel free to also swing by the [Network to Code Slack](https://networktocode.slack.com/) (channel `#nautobot`), sign up [here](http://slack.networktocode.com/) if you don't have an account.
