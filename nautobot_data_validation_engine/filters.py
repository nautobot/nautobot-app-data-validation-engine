"""Django filters."""

import django_filters as filters
from nautobot.apps.filters import NautobotFilterSet
from nautobot.extras.utils import FeatureQuery
from nautobot.utilities.filters import ContentTypeMultipleChoiceFilter, SearchFilter

from nautobot_data_validation_engine.models import (
    MinMaxValidationRule,
    RegularExpressionValidationRule,
    RequiredValidationRule,
    UniqueValidationRule,
    AuditRule,
)


class RegularExpressionValidationRuleFilterSet(NautobotFilterSet):
    """Base filterset for the RegularExpressionValidationRule model."""

    q = SearchFilter(
        filter_predicates={
            "name": "icontains",
            "slug": "icontains",
            "error_message": "icontains",
            "content_type__app_label": "equals",
            "content_type__model": "equals",
            "field": "equals",
            "regular_expression": "icontains",
        }
    )
    content_type = ContentTypeMultipleChoiceFilter(
        choices=FeatureQuery("custom_validators").get_choices, conjoined=False  # Make this an OR with multi-values
    )

    class Meta:
        """Filterset metadata for the RegularExpressionValidationRule model."""

        model = RegularExpressionValidationRule
        fields = [
            "id",
            "name",
            "slug",
            "regular_expression",
            "context_processing",
            "enabled",
            "content_type",
            "field",
            "error_message",
        ]


class MinMaxValidationRuleFilterSet(NautobotFilterSet):
    """Base filterset for the MinMaxValidationRule model."""

    q = SearchFilter(
        filter_predicates={
            "name": "icontains",
            "slug": "icontains",
            "error_message": "icontains",
            "content_type__app_label": "equals",
            "content_type__model": "equals",
            "field": "equals",
        }
    )
    content_type = ContentTypeMultipleChoiceFilter(
        choices=FeatureQuery("custom_validators").get_choices, conjoined=False  # Make this an OR with multi-values
    )

    class Meta:
        """Filterset metadata for the MinMaxValidationRuleFilterSet model."""

        model = MinMaxValidationRule
        fields = [
            "id",
            "name",
            "slug",
            "min",
            "max",
            "enabled",
            "content_type",
            "field",
            "error_message",
        ]


class RequiredValidationRuleFilterSet(NautobotFilterSet):
    """Base filterset for the RequiredValidationRule model."""

    q = SearchFilter(
        filter_predicates={
            "name": "icontains",
            "slug": "icontains",
            "error_message": "icontains",
            "content_type__app_label": "equals",
            "content_type__model": "equals",
            "field": "equals",
        }
    )
    content_type = ContentTypeMultipleChoiceFilter(
        choices=FeatureQuery("custom_validators").get_choices, conjoined=False  # Make this an OR with multi-values
    )

    class Meta:
        """Filterset metadata for the RequiredValidationRuleFilterSet model."""

        model = RequiredValidationRule
        fields = [
            "id",
            "name",
            "slug",
            "enabled",
            "content_type",
            "field",
            "error_message",
        ]


class UniqueValidationRuleFilterSet(NautobotFilterSet):
    """Base filterset for the UniqueValidationRule model."""

    q = SearchFilter(
        filter_predicates={
            "name": "icontains",
            "slug": "icontains",
            "error_message": "icontains",
            "content_type__app_label": "icontains",
            "content_type__model": "icontains",
            "field": "equals",
        }
    )
    content_type = ContentTypeMultipleChoiceFilter(
        choices=FeatureQuery("custom_validators").get_choices, conjoined=False  # Make this an OR with multi-values
    )

    class Meta:
        """Filterset metadata for the UniqueValidationRuleFilterSet model."""

        model = UniqueValidationRule
        fields = [
            "id",
            "name",
            "slug",
            "max_instances",
            "enabled",
            "content_type",
            "field",
            "error_message",
        ]


class AuditRuleFilterSet(NautobotFilterSet):
    """Base filterset for AuditRule model."""

    q = SearchFilter(
        filter_predicates={
            "class_name": "icontains",
            "method_name": "icontains",
            "message": "icontains",
            "content_type__app_label": "icontains",
            "content_type__model": "icontains",
            "object_id": "icontains",
        }
    )
    class_name = filters.CharFilter(field_name="class_name", lookup_expr="icontains")
    method_name = filters.CharFilter(field_name="method_name", lookup_expr="icontains")
    validated_attribute = filters.CharFilter(field_name="validated_attribute", lookup_expr="icontains")
    content_type = ContentTypeMultipleChoiceFilter(
        choices=FeatureQuery("audit rules").get_choices,
        conjoined=False,
    )

    class Meta:
        """Meta class for AuditRuleFilterSet."""

        model = AuditRule
        fields = ["class_name", "method_name", "valid"]
