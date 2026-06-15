"""Filtering for nautobot_data_validation_engine."""

from nautobot.apps.filters import NautobotFilterSet
from nautobot.core.filters import ContentTypeFilter, ContentTypeMultipleChoiceFilter, SearchFilter
from nautobot.extras.utils import FeatureQuery

from nautobot_data_validation_engine.models import (
    DataCompliance,
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
            "error_message": "icontains",
            "content_type__app_label": "iexact",
            "content_type__model": "iexact",
            "field": "iexact",
            "regular_expression": "icontains",
        }
    )
    content_type = ContentTypeMultipleChoiceFilter(
        choices=FeatureQuery("custom_validators").get_choices,
        conjoined=False,  # Make this an OR with multi-values
    )

    class Meta:
        """Filterset metadata for the RegularExpressionValidationRule model."""

        model = RegularExpressionValidationRule
        fields = "__all__"


class MinMaxValidationRuleFilterSet(NautobotFilterSet):
    """Base filterset for the MinMaxValidationRule model."""

    q = SearchFilter(
        filter_predicates={
            "name": "icontains",
            "error_message": "icontains",
            "content_type__app_label": "iexact",
            "content_type__model": "iexact",
            "field": "iexact",
        }
    )
    content_type = ContentTypeMultipleChoiceFilter(
        choices=FeatureQuery("custom_validators").get_choices,
        conjoined=False,  # Make this an OR with multi-values
    )

    class Meta:
        """Filterset metadata for the MinMaxValidationRuleFilterSet model."""

        model = MinMaxValidationRule
        fields = "__all__"


class RequiredValidationRuleFilterSet(NautobotFilterSet):
    """Base filterset for the RequiredValidationRule model."""

    q = SearchFilter(
        filter_predicates={
            "name": "icontains",
            "error_message": "icontains",
            "content_type__app_label": "iexact",
            "content_type__model": "iexact",
            "field": "iexact",
        }
    )
    content_type = ContentTypeMultipleChoiceFilter(
        choices=FeatureQuery("custom_validators").get_choices,
        conjoined=False,  # Make this an OR with multi-values
    )

    class Meta:
        """Filterset metadata for the RequiredValidationRuleFilterSet model."""

        model = RequiredValidationRule
        fields = "__all__"


class UniqueValidationRuleFilterSet(NautobotFilterSet):
    """Base filterset for the UniqueValidationRule model."""

    q = SearchFilter(
        filter_predicates={
            "name": "icontains",
            "error_message": "icontains",
            "content_type__app_label": "icontains",
            "content_type__model": "icontains",
            "field": "iexact",
        }
    )
    content_type = ContentTypeMultipleChoiceFilter(
        choices=FeatureQuery("custom_validators").get_choices,
        conjoined=False,  # Make this an OR with multi-values
    )

    class Meta:
        """Filterset metadata for the UniqueValidationRuleFilterSet model."""

        model = UniqueValidationRule
        fields = "__all__"


#
# DataCompliance
#


class DataComplianceFilterSet(NautobotFilterSet):
    """Base filterset for the DataCompliance model."""

    q = SearchFilter(
        filter_predicates={
            "compliance_class_name": "icontains",
            "message": "icontains",
            "content_type__app_label": "icontains",
            "content_type__model": "icontains",
            "object_id": "icontains",
        }
    )
    # DataCompliance records can reference any content type, so use the generic string-based
    # ``ContentTypeFilter`` (as core does for ObjectChange/Note) rather than
    # ``ContentTypeMultipleChoiceFilter``. The latter drives the advanced filter form to look up
    # this model's ``verbose_name_plural`` as a registered feature, which raises a ``KeyError`` for
    # "data compliance".
    content_type = ContentTypeFilter()

    class Meta:
        """Meta class for DataComplianceFilterSet."""

        model = DataCompliance
        fields = "__all__"
