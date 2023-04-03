"""Django tables."""

import django_tables2 as tables

from nautobot.utilities.tables import BaseTable, ToggleColumn

from nautobot_data_validation_engine.models import (
    MinMaxValidationRule,
    RegularExpressionValidationRule,
    RequiredValidationRule,
    UniqueValidationRule,
)


#
# RegularExpressionValidationRules
#


class RegularExpressionValidationRuleTable(BaseTable):
    """Base table for the RegularExpressionValidationRule model."""

    pk = ToggleColumn()
    name = tables.LinkColumn(order_by=("name",))

    class Meta(BaseTable.Meta):
        """Table metadata for the RegularExpressionValidationRule model."""

        model = RegularExpressionValidationRule
        fields = (
            "pk",
            "name",
            "enabled",
            "content_type",
            "field",
            "regular_expression",
            "context_processing",
            "error_message",
        )
        default_columns = (
            "pk",
            "name",
            "enabled",
            "content_type",
            "field",
            "regular_expression",
            "context_processing",
            "error_message",
        )


#
# MinMaxValidationRules
#


class MinMaxValidationRuleTable(BaseTable):
    """Base table for the MinMaxValidationRule model."""

    pk = ToggleColumn()
    name = tables.LinkColumn(order_by=("name",))

    class Meta(BaseTable.Meta):
        """Table metadata for the MinMaxValidationRuleTable model."""

        model = MinMaxValidationRule
        fields = (
            "pk",
            "name",
            "enabled",
            "content_type",
            "field",
            "min",
            "max",
            "error_message",
        )
        default_columns = (
            "pk",
            "name",
            "enabled",
            "content_type",
            "field",
            "min",
            "max",
            "error_message",
        )


#
# RequiredValidationRules
#


class RequiredValidationRuleTable(BaseTable):
    """Base table for the RequiredValidationRule model."""

    pk = ToggleColumn()
    name = tables.LinkColumn(order_by=("name",))

    class Meta(BaseTable.Meta):
        """Table metadata for the RequiredValidationRuleTable model."""

        model = RequiredValidationRule
        fields = (
            "pk",
            "name",
            "enabled",
            "content_type",
            "field",
            "error_message",
        )
        default_columns = (
            "pk",
            "name",
            "enabled",
            "content_type",
            "field",
            "error_message",
        )


#
# UniqueValidationRules
#


class UniqueValidationRuleTable(BaseTable):
    """Base table for the UniqueValidationRule model."""

    pk = ToggleColumn()
    name = tables.LinkColumn(order_by=("name",))

    class Meta(BaseTable.Meta):
        """Table metadata for the UniqueValidationRuleTable model."""

        model = UniqueValidationRule
        fields = (
            "pk",
            "name",
            "enabled",
            "content_type",
            "field",
            "max_instances",
            "error_message",
        )
        default_columns = (
            "pk",
            "name",
            "enabled",
            "content_type",
            "field",
            "max_instances",
            "error_message",
        )
