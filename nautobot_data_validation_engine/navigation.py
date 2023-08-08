"""Plugin navigation menu items."""

from nautobot.apps.ui import NavMenuGroup, NavMenuItem, NavMenuTab


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
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_data_validation_engine:regularexpressionvalidationrule_list",
                        name="Regex Rules",
                        permissions=["nautobot_data_validation_engine.view_regularexpressionvalidationrule"],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_data_validation_engine:requiredvalidationrule_list",
                        name="Required Rules",
                        permissions=["nautobot_data_validation_engine.view_requiredvalidationrule"],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_data_validation_engine:uniquevalidationrule_list",
                        name="Unique Rules",
                        permissions=["nautobot_data_validation_engine.view_uniquevalidationrule"],
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
