# v2.1 Release Notes

This document describes all new features and changes in the release `2.1`. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Release Overview

This release adds DataCompliance and DataComplianceRules to allow auditing of data within Nautobot programatically.

## [v2.1.1] - 2023-08-22

### Changed

- Dependency updates
- Additional Data Compliance docs and images
- Pin poetry to v1.5.1 due to dropping Python 3.7 support

### Fixed

- Fixed mkdocs bug encountered on Python 3.7
- Fixed bug where empty values were flagged by Unique Validation Rules
- Modified Unique Validation to exclude current object from unique count

## [v2.1.0] - 2023-05-17

### Added

- [#50] - Creation of DataCompliance and DataComplianceRules