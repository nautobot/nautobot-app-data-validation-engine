# v2.0 Release Notes

This document describes all new features and changes in the release `2.0`. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Release Overview

This release contains major new rule types and changes to UI & API behaviour

## [v2.0.0] - 2023-04-04

### Added

- [#15] - Added the required field validation rule type
- [#20] - Added the unique field validation rule type
- [#28] - Added support for Jinja2 template context rendering in regular expression validation rules

### Changed

- The UI navigation dropdown menu items have been moved to the Extensibility tab
- The UI URL routes for regular expression and min/max rules have been changed:
    - Regular expression rules are now located at `/plugins/data-validation-engine/regex-rules/`
    - Min/max rules are now located at `/plugins/data-validation-engine/min-max-rules/`
- The REST API routes for regular expression and min/max rules have been changed:
    - Regular expression rules are now located at `/api/plugins/data-validation-engine/regex-rules/`
    - Min/max rules are now located at `/api/plugins/data-validation-engine/min-max-rules/`
- The plugin's code has been refactored to align with the `cookiecutter-ntc` template
