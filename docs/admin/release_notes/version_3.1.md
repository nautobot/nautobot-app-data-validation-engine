# v3.1 Release Notes

This document describes all new features and changes in the release `3.1`. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Release Overview

This release adds additional functionality to the Data Compliance feature with the ability to now include built-in data validation rules.

## [v3.1.1 (2024-04-15)](https://github.com/nautobot/nautobot-app-data-validation-engine/releases/tag/v3.1.1)

### Security

- [#144](https://github.com/nautobot/nautobot-app-data-validation-engine/issues/144) - Updated `cryptography` dependency to 42.0.0 due to CVE-2023-50782.
- [#145](https://github.com/nautobot/nautobot-app-data-validation-engine/issues/145) - Updated `django` dependency to `3.2.24` due to CVE-2024-24680.
- [#148](https://github.com/nautobot/nautobot-app-data-validation-engine/issues/148) - Updated `cryptography` dependency to 42.0.4 due to CVE-2024-26130 and CVE-2024-0727.
- [#153](https://github.com/nautobot/nautobot-app-data-validation-engine/issues/153) - Updated `django` dependency to `3.2.25` due to CVE-2024-27351.
- [#154](https://github.com/nautobot/nautobot-app-data-validation-engine/issues/154) - Updated `black` dependency to `24.3.0` due to CVE-2024-21503.
- [#157](https://github.com/nautobot/nautobot-app-data-validation-engine/issues/157) - Updated `idna` dependency to `3.7` due to CVE-2024-3651.

### Fixed

- [#155](https://github.com/nautobot/nautobot-app-data-validation-engine/issues/155) - Fixed issues where going to "Data Compliance" tab could potentially hide other tabs.

### Housekeeping

- [#150](https://github.com/nautobot/nautobot-app-data-validation-engine/issues/150), [#152](https://github.com/nautobot/nautobot-app-data-validation-engine/issues/152) - Re-baked from the latest template.

## v3.1.0 (2024-02-02)

### Added

- Added built-in validation rules (Min/Max, Regex, Required, Unique) to Data Compliance.
- Added check-box option to Data Compliance job for built-in rules.
- Added link to Data Compliance results within job logging.

### Changed

- [#141](https://github.com/nautobot/nautobot-app-data-validation-engine/issues/141) - Replaced pydocstyle with ruff.
- Updated compliance job logging.
- Updated data compliance comments.
- Updated with drift manager inconsistencies.
