"""Django filters."""

from nautobot.apps.filters import NautobotFilterSet
from nautobot.extras.utils import FeatureQuery
from nautobot.utilities.filters import ContentTypeMultipleChoiceFilter, SearchFilter

from nautobot_data_validation_engine.models import (
    MinMaxValidationRule,
    RegularExpressionValidationRule,
    RequiredValidationRule,
    UniqueValidationRule,
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
            "content_type__app_label": "equals",
            "content_type__model": "equals",
            "field": "equals",
        }
    )
    content_type = ContentTypeMultipleChoiceFilter(
        choices=FeatureQuery("custom_validators").get_choices, conjoined=False  # Make this an OR with multi-values
    )

    class Meta:
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
