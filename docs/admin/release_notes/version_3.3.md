# v3.3 Release Notes

This document describes all new features and changes in the release. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Release Overview

- Removed support for Nautobot <2.4
- Removed support for Python 3.8
- Added support for Python 3.12

## [v3.3.0 (2025-10-08)](https://github.com/nautobot/nautobot-app-data-validation-engine/releases/tag/v3.3.0)

### Fixed

- [#181](https://github.com/nautobot/nautobot-app-data-validation-engine/issues/181) - Replaced all occurrences of PluginCustomValidator with CustomValidator.
- [#191](https://github.com/nautobot/nautobot-app-data-validation-engine/issues/191) - Correct class inheritance on Bulk Edit Forms to resolve issue loading the Bulk Edit Views.
- [#210](https://github.com/nautobot/nautobot-app-data-validation-engine/issues/210) - Fixed a race condition when discovering/importing data compliance rules from a Git repository.

### Dependencies

- Removed support for Nautobot <2.4.
- Removed support for Python 3.8.
- Added support for Python 3.12.

### Housekeeping

- [#215](https://github.com/nautobot/nautobot-app-data-validation-engine/issues/215) - Fixed incorrectly named UIViewSet for DataCompliance.
- Rebaked from the cookie `nautobot-app-v2.4.1`.
- Rebaked from the cookie `nautobot-app-v2.4.2`.
- Rebaked from the cookie `nautobot-app-v2.5.0`.
- Rebaked from the cookie `nautobot-app-v2.5.1`.
- Rebaked from the cookie `nautobot-app-v2.6.0`.
