# v3.1 Release Notes

This document describes all new features and changes in the release `3.1`. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Release Overview

This release adds additional functionality to the Data Compliance feature with the ability to now include built-in data validation rules.

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
