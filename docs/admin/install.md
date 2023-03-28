# Installing the App in Nautobot

Here you will find detailed instructions on how to **install** and **configure** the App within your Nautobot environment.

## Prerequisites

- This Nautobot App is compatible with Nautobot 1.0.0 and higher.
- Databases supported: PostgreSQL, MySQL

!!! note
    Please check the [dedicated page](compatibility_matrix.md) for a full compatibility matrix and the deprecation policy.

### Access Requirements

## Install Guide

!!! note
    Nautobot Apps can be installed manually or using Python's `pip`. See the [nautobot documentation](https://nautobot.readthedocs.io/en/latest/plugins/#install-the-package) for more details. The pip package name for this Nautobot App 
    is [`nautobot-data-validation-engine`](https://pypi.org/project/nautobot-data-validation-engine/).

This Nautobot App is available as a Python package via PyPI and can be installed with `pip`:

```shell
pip install nautobot-data-validation-engine
```

To ensure Data Validation Engine is automatically re-installed during future upgrades, create a file named `local_requirements.txt` (if not already existing) in the Nautobot root directory (alongside `requirements.txt`) and list the `nautobot-data-validation-engine` package:

```shell
echo nautobot-data-validation-engine >> local_requirements.txt
```

Once installed, this Nautobot App needs to be enabled in your Nautobot configuration. The following block of code below shows the additional configuration required to be added to your `nautobot_config.py` file:

- Append `"nautobot_data_validation_engine"` to the `NAUTOBOT_APPS` list.
- Append the `"nautobot_data_validation_engine"` dictionary to the `NAUTOBOT_APPS_CONFIG` dictionary and override any defaults.

```python
# In your nautobot_config.py
NAUTOBOT_APPS = ["nautobot_data_validation_engine"]

# NAUTOBOT_APPS_CONFIG = {
#   "nautobot_data_validation_engine": {
#     ADD YOUR SETTINGS HERE
#   }
# }
```

Once the Nautobot configuration is updated, run the Post Upgrade command (`nautobot-server post_upgrade`) to run migrations and clear any cache:

```shell
nautobot-server post_upgrade
```

Then restart (if necessary) the Nautobot services which may include:

- Nautobot
- Nautobot Workers
- Nautobot Scheduler

```shell
sudo systemctl restart nautobot nautobot-worker nautobot-scheduler
```

## App Configuration