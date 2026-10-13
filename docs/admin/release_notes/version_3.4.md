# v3.4 Release Notes

This document describes all new features and changes in the release. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Release Overview

The functionality of this app has been moved to Nautobot as of [version 3.0.0](https://docs.nautobot.com/projects/core/en/stable/release-notes/version-3.0/). The 3.4.x release of this app will continue to support Nautobot v2.4.x and will be maintained for security and critical bug fixes only. All new feature requests for data validation should go directly to [Nautobot](https://github.com/nautobot/nautobot).

- Fixed Python 3.12 compatibility issues.
- Changed minimum Nautobot version to 2.4.20.
- Dropped support for Python 3.9.

<!-- towncrier release notes start -->

## [v3.4.1 (2026-10-13)](https://github.com/nautobot/nautobot-app-data-validation-engine/releases/tag/v3.4.1)

### Security

- [#GHSA-59j7-mhqh-vq5w](https://github.com/nautobot/nautobot-app-data-validation-engine/security/advisories/GHSA-59j7-mhqh-vq5w) - Added a timeout to regular expression evaluation in the data validation engine, to protect against denial of service (REDoS) due to an overly-complex or maliciously crafted regular expression.
- [#GHSA-x5gx-4x5h-3rp5](https://github.com/nautobot/nautobot-app-data-validation-engine/security/advisories/GHSA-x5gx-4x5h-3rp5) - Stopped the data being validated from influencing the structure of a `RegularExpressionValidationRule` regular expression that uses Jinja2 context processing, to protect against bypass of a validation rule.

### Changed

- [#GHSA-x5gx-4x5h-3rp5](https://github.com/nautobot/nautobot-app-data-validation-engine/security/advisories/GHSA-x5gx-4x5h-3rp5) - Values interpolated into a `RegularExpressionValidationRule` regular expression via Jinja2 context processing are now escaped and treated as literal text, so that the data being validated can no longer alter the structure of the pattern. Rules that deliberately drew regular expression syntax from a field value will no longer behave the same way.

### Dependencies

- [#GHSA-59j7-mhqh-vq5w](https://github.com/nautobot/nautobot-app-data-validation-engine/security/advisories/GHSA-59j7-mhqh-vq5w) - Added `regex` as an explicit dependency to support time-bounded evaluation of regular expressions.

### Housekeeping

- Rebaked from the cookie `nautobot-app-v2.7.2`.
- Rebaked from the cookie `nautobot-app-v2.7.3`.

## [v3.4.0 (2025-12-05)](https://github.com/nautobot/nautobot-app-data-validation-engine/releases/tag/v3.4.0)

### Fixed

- [#204](https://github.com/nautobot/nautobot-app-data-validation-engine/issues/204) - Fixed Python 3.12 compatibility issues.
- [#218](https://github.com/nautobot/nautobot-app-data-validation-engine/issues/218) - Updated rendering of boolean fields in rule tables to match the Nautobot standard.

### Documentation

- [#207](https://github.com/nautobot/nautobot-app-data-validation-engine/issues/207) - Added Analytics GTM template override only to the public ReadTheDocs build.

### Housekeeping

- Rebaked from the cookie `nautobot-app-v2.7.0`.
- Rebaked from the cookie `nautobot-app-v2.7.1`.
