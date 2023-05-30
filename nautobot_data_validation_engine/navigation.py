# """Plugin navigation menu items."""

from nautobot.core.apps import NavMenuGroup, NavMenuItem, NavMenuTab


menu_items = (
    NavMenuTab(
        name="Platform",
        groups=(
            NavMenuGroup(
                name="Data Validation",
                weight=405,
                items=(
                    NavMenuItem(
                        weight=100,
                        link="plugins:nautobot_data_validation_engine:minmaxvalidationrule_list",
                        name="Min/Max Rules",
                        permissions=["nautobot_data_validation_engine.view_minmaxvalidationrule"],
                    ),
                    NavMenuItem(
                        weight=200,
                        link="plugins:nautobot_data_validation_engine:regularexpressionvalidationrule_list",
                        name="Regex Rules",
                        permissions=["nautobot_data_validation_engine.view_regularexpressionvalidationrule"],
                    ),
                    NavMenuItem(
                        weight=300,
                        link="plugins:nautobot_data_validation_engine:requiredvalidationrule_list",
                        name="Required Rules",
                        permissions=["nautobot_data_validation_engine.view_requiredvalidationrule"],
                    ),
                    NavMenuItem(
                        weight=400,
                        link="plugins:nautobot_data_validation_engine:uniquevalidationrule_list",
                        name="Unique Rules",
                        permissions=["nautobot_data_validation_engine.view_uniquevalidationrule"],
                    ),
                    NavMenuItem(
                        weight=500,
                        link="plugins:nautobot_data_validation_engine:datacompliance_list",
                        name="Data Compliance",
                        permissions=["nautobot_data_validation_engine.view_datacompliance"],
                    ),
                ),
            ),
        ),
    ),
)
