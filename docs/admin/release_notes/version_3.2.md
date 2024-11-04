# v3.2 Release Notes

This document describes all new features and changes in the release. The format is based on [Keep a
Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic
Versioning](https://semver.org/spec/v2.0.0.html).

## Release Overview

- Now supports Python 3.12.

## [v3.2.0 (2024-11-04)](https://github.com/nautobot/nautobot-app-data-validation-engine/releases/tag/v3.2.0)

### Security

- [#160](https://github.com/nautobot/nautobot-app-data-validation-engine/issues/160) - Updated `sqlparse` dependency to `0.5.0` due to GHSA-2m57-hf25-phgg.
- [#163](https://github.com/nautobot/nautobot-app-data-validation-engine/issues/163) - Updated `jinja2` dependency to `3.1.4` due to CVE-2024-34064.
- [#167](https://github.com/nautobot/nautobot-app-data-validation-engine/issues/167) - Updated `requests` dependency to `2.32.2` due to CVE-2024-35195.
- [#171](https://github.com/nautobot/nautobot-app-data-validation-engine/issues/171) - Updated `urllib3` dependency to `2.2.2` due to CVE-2024-37891.

### Added

- [#162](https://github.com/nautobot/nautobot-app-data-validation-engine/issues/162) - Added view name to `OrderedDefaultRouter`.
- [#177](https://github.com/nautobot/nautobot-app-data-validation-engine/issues/177) - Added support for Python 3.12.
- [#183](https://github.com/nautobot/nautobot-app-data-validation-engine/issues/183) - Added support for filtering by Compliance Class Name with a name longer than twenty characters and to filter by multiple names at the same time.

### Changed

- [#146](https://github.com/nautobot/nautobot-app-data-validation-engine/issues/146) - Updated app images with screenshots from Nautobot 2.X UI.
- [#146](https://github.com/nautobot/nautobot-app-data-validation-engine/issues/146) - Changed references of `site` to `location` in docs.
- [#162](https://github.com/nautobot/nautobot-app-data-validation-engine/issues/162) - Updated minimum Nautobot version to `2.1.9`.
- [#162](https://github.com/nautobot/nautobot-app-data-validation-engine/issues/162) - Disabled specific `nb-use-fields-all` and `nb-sub-class-name` pylint rules in `tables.py`.

### Removed

- [#162](https://github.com/nautobot/nautobot-app-data-validation-engine/issues/162) - Removed `DataValidationEngineRootView` class and `APIRootView` override.
- [#162](https://github.com/nautobot/nautobot-app-data-validation-engine/issues/162) - Removed `version` from docker-compose files.
- [#163](https://github.com/nautobot/nautobot-app-data-validation-engine/issues/163) - Removed authentication/password command from MySQL Docker Compose.

### Housekeeping

- [#0](https://github.com/nautobot/nautobot-app-data-validation-engine/issues/0) - Rebaked from the cookie `nautobot-app-v2.4.0`.
- [#174](https://github.com/nautobot/nautobot-app-data-validation-engine/issues/174) - Rebake with 2.3.0 Cookiecutter.
- [#177](https://github.com/nautobot/nautobot-app-data-validation-engine/issues/177) - Rebaked with nautobot-app-v2.3.2 Cookiecutter.
- [#185](https://github.com/nautobot/nautobot-app-data-validation-engine/issues/185) - Changed model_class_name in .cookiecutter.json to a valid model to help with drift management.
