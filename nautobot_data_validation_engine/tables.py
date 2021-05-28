"""
Django tables.
"""
import django_tables2 as tables

from nautobot.utilities.tables import BaseTable, ToggleColumn

from nautobot_data_validation_engine.models import MinMaxValidationRule, RegularExpressionValidationRule


#
# RegularExpressionValidationRules
#


class RegularExpressionValidationRuleTable(BaseTable):
    """
    Base table for the RegularExpressionValidationRule model.
    """

    pk = ToggleColumn()
    name = tables.LinkColumn(order_by=("name",))

    class Meta(BaseTable.Meta):
        model = RegularExpressionValidationRule
        fields = ("pk", "name", "enabled", "content_type", "field", "regular_expression", "error_message")
        default_columns = ("pk", "name", "enabled", "content_type", "field", "regular_expression", "error_message")


#
# MinMaxValidationRules
#


class MinMaxValidationRuleTable(BaseTable):
    """
    Base table for the MinMaxValidationRule model.
    """

    pk = ToggleColumn()
    name = tables.LinkColumn(order_by=("name",))

    class Meta(BaseTable.Meta):
        model = MinMaxValidationRule
        fields = ("pk", "name", "enabled", "content_type", "field", "min", "max", "error_message")
        default_columns = ("pk", "name", "enabled", "content_type", "field", "min", "max", "error_message")
