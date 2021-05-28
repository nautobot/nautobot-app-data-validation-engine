"""
Plugin navigation menu items.
"""
from nautobot.extras.plugins import PluginMenuButton, PluginMenuItem
from nautobot.utilities.choices import ButtonColorChoices


menu_items = (
    PluginMenuItem(
        link="plugins:nautobot_data_validation_engine:minmaxvalidationrule_list",
        link_text="Min/Max Rules",
        permissions=["nautobot_data_validation_engine.view_minmaxvalidationrule"],
        buttons=(
            PluginMenuButton(
                link="plugins:nautobot_data_validation_engine:minmaxvalidationrule_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
                permissions=["nautobot_data_validation_engine.add_minmaxvalidationrule"],
            ),
            PluginMenuButton(
                link="plugins:nautobot_data_validation_engine:minmaxvalidationrule_import",
                title="Import",
                icon_class="mdi mdi-database-import-outline",
                color=ButtonColorChoices.BLUE,
                permissions=["nautobot_data_validation_engine.add_minmaxvalidationrule"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:nautobot_data_validation_engine:regularexpressionvalidationrule_list",
        link_text="Regex Rules",
        permissions=["nautobot_data_validation_engine.view_regularexpressionvalidationrule"],
        buttons=(
            PluginMenuButton(
                link="plugins:nautobot_data_validation_engine:regularexpressionvalidationrule_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
                permissions=["nautobot_data_validation_engine.add_regularexpressionvalidationrule"],
            ),
            PluginMenuButton(
                link="plugins:nautobot_data_validation_engine:regularexpressionvalidationrule_import",
                title="Import",
                icon_class="mdi mdi-database-import-outline",
                color=ButtonColorChoices.BLUE,
                permissions=["nautobot_data_validation_engine.add_regularexpressionvalidationrule"],
            ),
        ),
    ),
)
