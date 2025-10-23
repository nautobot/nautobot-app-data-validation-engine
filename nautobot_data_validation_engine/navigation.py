"""Menu items."""

from nautobot.apps.ui import NavMenuAddButton, NavMenuGroup, NavMenuItem, NavMenuTab

items = (
    NavMenuItem(
        link="plugins:nautobot_data_validation_engine:regularexpressionvalidationrule_list",
        name="Data Validation Engine",
        permissions=["nautobot_data_validation_engine.view_regularexpressionvalidationrule"],
        buttons=(
            NavMenuAddButton(
                link="plugins:nautobot_data_validation_engine:regularexpressionvalidationrule_add",
                permissions=["nautobot_data_validation_engine.add_regularexpressionvalidationrule"],
            ),
        ),
    ),
)

menu_items = (
    NavMenuTab(
        name="Apps",
        groups=(NavMenuGroup(name="Data Validation Engine", items=tuple(items)),),
    ),
)
