# v2.3 Release Notes

This document describes all new features and changes in the release `2.3`. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Release Overview

This release adds support for Nautobot v2.0.0.

## [v2.3.0] - 2023-09-29

### Changed

- All Nautobot 2.0.0 compatibility changes from `v2.3.0-rc.1`
- Dependency updates

## [v2.3.0-rc.1] - 2023-09-14

### Added

- Added Tags to validation rules
- Added `pylint-nautobot`
- Re-added healthcheck to `docker-compose`
- Added `0004_created_datetime` migration
- Added `0005_remove_slugs_alter_tags` migration
- Uses natural_key in place of slugs

### Changed

- Nautobot v2.0 updates following `from-v1` migration guides
- Changed rule urls to use UUID instead of slug
- Changed LogLevelChoices.LOG_SUCCESS to __.LOG_INFO
- Updated jobs logging and restering
- Moved from Site & Region to Location model
- Changed filter fields to use `__all__`
- Updates to form parent classes
- Dependency updates

### Removed

- Removed the use of slugs
- Removed nested serializers
