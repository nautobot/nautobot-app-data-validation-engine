# Nautobot Data Validation Engine Plugin

A plugin for [Nautobot](https://github.com/nautobot/nautobot) with a UI to build custom data validation rules for data.

## Installation

If using the installation pattern from the Nautobot Documentation, you will need to activate the
virtual environment before installing so that you install the package into the virtual environment.

```shell
cd /opt/nautobot
source venv/bin/activate
```

The plugin is available as a Python package in pypi and can be installed with pip. Once the
installation is completed, then Nautobot and the Nautobot worker must be restarted.

```shell
pip install nautobot-data-validation-engine
systemctl restart nautobot nautobot-rq
```

To ensure Data Validation Engine plugin is automatically re-installed during future upgrades, create a file named `local_requirements.txt` (if not already existing) in the Nautobot root directory (alongside `requirements.txt`) and list the `nautobot-data-validation-engine` package:

```no-highlight
# echo nautobot-data-validation-engine >> local_requirements.txt
```

Once installed, the plugin needs to be enabled in your `nautobot_config.py`
```python
# In your configuration.py
PLUGINS = ["nautobot_data_validation_engine"]

# PLUGINS_CONFIG = {
#   "nautobot_data_validation_engine": {
#     ADD YOUR SETTINGS HERE
#   }
# }
```

Finally, make sure to run the migrations for this plugin

```bash
nautobot-server migrate
```

## Upgrades

When a new release comes out it may be necessary to run a migration of the database to account for any changes in the data models used by this plugin. Execute the command `nautobot-server migrate` from the Nautobot install `nautobot/` directory after updating the package.

## Usage

TODO

## Contributing

Pull requests are welcomed and automatically built and tested against multiple version of Python and multiple version of Nautobot through TravisCI.

The project is packaged with a light development environment based on `docker-compose` to help with the local development of the project and to run the tests within TravisCI.

The project is following Network to Code software development guideline and is leveraging:
- Black, Pylint, Bandit and pydocstyle for Python linting and formatting.
- Django unit test to ensure the plugin is working properly.

### CLI Helper Commands

The project is coming with a CLI helper based on [invoke](http://www.pyinvoke.org/) to help setup the development environment. The commands are listed below in 3 categories `dev environment`, `utility` and `testing`. 

Each command can be executed with `invoke <command>`. All commands support the arguments `--nautobot-ver` and `--python-ver` if you want to manually define the version of Python and Nautobot to use. Each command also has its own help `invoke <command> --help`

#### Local dev environment
```
  build            Build all docker images.
  debug            Start Nautobot and its dependencies in debug mode.
  destroy          Destroy all containers and volumes.
  start            Start Nautobot and its dependencies in detached mode.
  stop             Stop Nautobot and its dependencies.
```

#### Utility 
```
  cli              Launch a bash shell inside the running Nautobot container.
  create-user      Create a new user in django (default: admin), will prompt for password.
  makemigrations   Run Make Migration in Django.
  nbshell          Launch a nbshell session.
```
#### Testing 

```
  tests            Run all tests for this plugin.
  pylint           Run pylint code analysis.
  pydocstyle       Run pydocstyle to validate docstring formatting adheres to NTC defined standards.
  bandit           Run bandit to validate basic static code security analysis.
  black            Run black to check that Python files adhere to its style standards.
  unittest         Run Django unit tests for the plugin.
```

## Questions

For any questions or comments, please check the [FAQ](FAQ.md) first and feel free to swing by the [Network to Code slack channel](https://networktocode.slack.com/) (channel #networktocode).
Sign up [here](http://slack.networktocode.com/)

## Screenshots

