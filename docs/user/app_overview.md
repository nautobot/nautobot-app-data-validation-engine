# App Overview

This document provides an overview of the App including critical information and import considerations when applying it to your Nautobot environment.

!!! note
    Throughout this documentation, the terms "app" and "plugin" will be used interchangeably.

## Description

The data validation engine app offers a set of user definable rules which are used to enforce business constraints on the data in Nautobot. These rules are tied to particular models and each rule is meant to enforce one aspect of a business use case.

Supported rule types include:
- Regular expression
- Min/max value
- Required fields
- Unique values

## Audience (User Personas) - Who should use this App?

Network Engineers interested in Network Automation, Infrastructure as Code, etc., that need to add some custom validation to their data input process.

## Authors and Maintainers

- John Anderson (@lampwins)
