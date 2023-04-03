# Getting Started with the App

This document provides a step-by-step tutorial on how to get the App going and how to use it.

## Install the App

To install the App, please follow the instructions detailed in the [Installation Guide](../admin/install.md).

## First steps with the App

Once the App is installed, under the "Extensibility" tab, you will find the supported Data Validation Engine rules in the "Data Validation" section. For example, "Min/Max Rules" or "Regex Rules".

There you can list the existing validation rules of each type, or create them (one by one, or dumping them).

!!! note
    The validation rules only take effect for new data entries, not for previous existing data. So, when you create a new object, for instance, an `ipam.VLAN`, that is when the existing validation rules will be enforced. Validation rules will be enforced when explicitly editing existing data.
