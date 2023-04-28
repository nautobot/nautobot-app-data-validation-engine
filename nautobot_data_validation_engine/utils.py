"""Utility functions for nautobot_data_validation_engine."""

# import inspect
# import pkgutil
# from nautobot.extras.registry import registry
# from nautobot.extras.models import GitRepository
# from nautobot.extras.datasources import ensure_git_repository


# def get_data_compliance_rules_map():
#     """Generate a dictionary of audit rulesets associated to their models."""
#     from .custom_validators import is_data_compliance_rule

#     compliance_rulesets = {}
#     for validators in registry["plugin_custom_validators"].values():
#         for validator in validators:
#             if is_data_compliance_rule(validator):
#                 compliance_rulesets.setdefault(validator.model, [])
#                 compliance_rulesets[validator.model].append(validator)

#     return compliance_rulesets


# def get_data_compliance_rules():
#     """Generate a list of Audit Ruleset classes that exist from the registry."""
#     validators = []
#     for rule_sets in get_data_compliance_rules_map().values():
#         validators.extend(rule_sets)
#     return validators


# def get_classes_from_git_repo(repo: GitRepository):
#     """Get list of DataComplianceRule classes found within the custom_validators folder of the given repo."""
#     from .custom_validators import is_data_compliance_rule

#     ensure_git_repository(repo)
#     class_list = []
#     for importer, discovered_module_name, _ in pkgutil.iter_modules([f"{repo.filesystem_path}/custom_validators"]):
#         module = importer.find_module(discovered_module_name).load_module(discovered_module_name)
#         for _, complance_class in inspect.getmembers(module, is_data_compliance_rule):
#             class_list.append(complance_class)
#     return class_list
