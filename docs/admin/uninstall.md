# Uninstall the App from Nautobot

Here you will find any steps necessary to cleanly remove the App from your Nautobot environment.

## Uninstall Guide

Remove the configuration you added in `nautobot_config.py` from `NAUTOBOT_APPS` & `NAUTOBOT_APPS_CONFIG`.

## Database Cleanup

Drop all tables from the Nautobot App: `nautobot_plugin_data_validation_engine*`.
