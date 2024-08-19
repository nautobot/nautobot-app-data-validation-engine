"""App navigation menu items."""

from nautobot.apps.ui import NavMenuAddButton, NavMenuGroup, NavMenuImportButton, NavMenuItem, NavMenuTab

menu_items = (
    NavMenuTab(
        name="Extensibility",
        groups=(
            NavMenuGroup(
                name="Data Validation Engine",
                weight=200,
                items=(
                    NavMenuItem(
                        link="plugins:nautobot_data_validation_engine:minmaxvalidationrule_list",
                        name="Min/Max Rules",
                        permissions=["nautobot_data_validation_engine.view_minmaxvalidationrule"],
                        buttons=(
                            NavMenuAddButton(
                                link="plugins:nautobot_data_validation_engine:minmaxvalidationrule_add",
                                permissions=["nautobot_data_validation_engine.add_minmaxvalidationrule"],
                            ),
                            NavMenuImportButton(
                                link="plugins:nautobot_data_validation_engine:minmaxvalidationrule_import",
                                permissions=["nautobot_data_validation_engine.add_minmaxvalidationrule"],
                            ),
                        ),
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_data_validation_engine:regularexpressionvalidationrule_list",
                        name="Regex Rules",
                        permissions=["nautobot_data_validation_engine.view_regularexpressionvalidationrule"],
                        buttons=(
                            NavMenuAddButton(
                                link="plugins:nautobot_data_validation_engine:regularexpressionvalidationrule_add",
                                permissions=["nautobot_data_validation_engine.add_regularexpressionvalidationrule"],
                            ),
                            NavMenuImportButton(
                                link="plugins:nautobot_data_validation_engine:regularexpressionvalidationrule_import",
                                permissions=["nautobot_data_validation_engine.add_regularexpressionvalidationrule"],
                            ),
                        ),
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_data_validation_engine:requiredvalidationrule_list",
                        name="Required Rules",
                        permissions=["nautobot_data_validation_engine.view_requiredvalidationrule"],
                        buttons=(
                            NavMenuAddButton(
                                link="plugins:nautobot_data_validation_engine:requiredvalidationrule_add",
                                permissions=["nautobot_data_validation_engine.add_requiredvalidationrule"],
                            ),
                            NavMenuImportButton(
                                link="plugins:nautobot_data_validation_engine:requiredvalidationrule_import",
                                permissions=["nautobot_data_validation_engine.add_requiredvalidationrule"],
                            ),
                        ),
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_data_validation_engine:uniquevalidationrule_list",
                        name="Unique Rules",
                        permissions=["nautobot_data_validation_engine.view_uniquevalidationrule"],
                        buttons=(
                            NavMenuAddButton(
                                link="plugins:nautobot_data_validation_engine:uniquevalidationrule_add",
                                permissions=["nautobot_data_validation_engine.add_uniquevalidationrule"],
                            ),
                            NavMenuImportButton(
                                link="plugins:nautobot_data_validation_engine:uniquevalidationrule_import",
                                permissions=["nautobot_data_validation_engine.add_uniquevalidationrule"],
                            ),
                        ),
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_data_validation_engine:datacompliance_list",
                        name="Data Compliance",
                        permissions=["nautobot_data_validation_engine.view_datacompliance"],
                    ),
                ),
            ),
        ),
    ),
)
