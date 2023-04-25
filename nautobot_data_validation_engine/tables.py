"""Django tables."""

import django_tables2 as tables
from django.utils.safestring import mark_safe

from nautobot.utilities.tables import BaseTable, ToggleColumn

from nautobot_data_validation_engine.models import (
    MinMaxValidationRule,
    RegularExpressionValidationRule,
    RequiredValidationRule,
    UniqueValidationRule,
    Audit,
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


class ValidatedAttributeColumn(tables.Column):
    """Column that links to the object's attribute if it is linkable."""

    def render(self, value, record):  # pylint: disable=W0221
        """Generate a link to a validated attribute if it is linkable, otherwise return the attribute."""
        if hasattr(record.validated_object, value) and hasattr(
            getattr(record.validated_object, value), "get_absolute_url"
        ):
            return mark_safe(
                f'<a href="{getattr(record.validated_object, value).get_absolute_url()}">{value}</a>'
            )  # nosec B703, B308
        return value


class AuditTable(BaseTable):
    """Base table for viewing all Audit Rules."""

    pk = ToggleColumn()
    id = tables.Column(linkify=True, verbose_name="ID")
    validated_object = tables.RelatedLinkColumn()
    validated_attribute = ValidatedAttributeColumn()

    class Meta(BaseTable.Meta):
        """Meta class for AuditRuleTable."""

        model = Audit
        fields = [
            "pk",
            "id",
            "content_type",
            "audit_class_name",
            "last_validation_date",
            "validated_object",
            "validated_attribute",
            "validated_attribute_value",
            "valid",
            "message",
        ]
        default_columns = [
            "pk",
            "id",
            "content_type",
            "audit_class_name",
            "last_validation_date",
            "validated_object",
            "validated_attribute",
            "validated_attribute_value",
            "valid",
            "message",
        ]


class AuditTableTab(BaseTable):
    """Base table for viewing the Audit Rules related to a single object."""

    validated_attribute = ValidatedAttributeColumn()

    class Meta(BaseTable.Meta):
        """Meta class for AuditTableTab."""

        model = Audit
        fields = [
            "content_type",
            "audit_class_name",
            "last_validation_date",
            "validated_attribute",
            "validated_attribute_value",
            "valid",
            "message",
        ]
        default_columns = [
            "content_type",
            "audit_class_name",
            "last_validation_date",
            "validated_attribute",
            "validated_attribute_value",
            "valid",
            "message",
        ]
