"""Django filters."""

import django_filters as filters
from django.db import models

from nautobot.apps.filters import NautobotFilterSet
from nautobot.core.filters import ContentTypeMultipleChoiceFilter, SearchFilter, TagFilter
from nautobot.extras.utils import FeatureQuery

from nautobot_data_validation_engine.models import (
    MinMaxValidationRule,
    RegularExpressionValidationRule,
    RequiredValidationRule,
    UniqueValidationRule,
    DataCompliance,
)


class RegularExpressionValidationRuleFilterSet(NautobotFilterSet):
    """Base filterset for the RegularExpressionValidationRule model."""

    q = SearchFilter(
        filter_predicates={
            "name": "icontains",
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
    tag = TagFilter()

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
            "content_type__app_label": "equals",
            "content_type__model": "equals",
            "field": "equals",
        }
    )
    content_type = ContentTypeMultipleChoiceFilter(
        choices=FeatureQuery("custom_validators").get_choices, conjoined=False  # Make this an OR with multi-values
    )
    tag = TagFilter()

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
            "content_type__app_label": "equals",
            "content_type__model": "equals",
            "field": "equals",
        }
    )
    content_type = ContentTypeMultipleChoiceFilter(
        choices=FeatureQuery("custom_validators").get_choices, conjoined=False  # Make this an OR with multi-values
    )
    tag = TagFilter()

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
            "field": "equals",
        }
    )
    content_type = ContentTypeMultipleChoiceFilter(
        choices=FeatureQuery("custom_validators").get_choices, conjoined=False  # Make this an OR with multi-values
    )
    tag = TagFilter()

    class Meta:
        """Filterset metadata for the UniqueValidationRuleFilterSet model."""

        model = UniqueValidationRule
        fields = "__all__"


#
# DataCompliance
#


class CustomContentTypeFilter(filters.MultipleChoiceFilter):
    """Filter for ContentType that doesn't rely on the model's plural name to be in the registry."""

    def filter(self, qs, value):
        """Filter on value, which should be list of content-type names.

        e.g. `['dcim.device', 'dcim.rack']`
        """
        q = models.Q()
        for v in value:
            try:
                app_label, model = v.lower().split(".")
            except ValueError:
                continue
            q |= models.Q(
                **{
                    f"{self.field_name}__app_label": app_label,
                    f"{self.field_name}__model": model,
                }
            )
        qs = qs.filter(q)
        return qs


class DataComplianceFilterSet(NautobotFilterSet):
    """Base filterset for DataComplianceRule model."""

    q = SearchFilter(
        filter_predicates={
            "compliance_class_name": "icontains",
            "message": "icontains",
            "content_type__app_label": "icontains",
            "content_type__model": "icontains",
            "object_id": "icontains",
        }
    )
    content_type = CustomContentTypeFilter(
        choices=FeatureQuery("custom_validators").get_choices,
    )

    class Meta:
        """Meta class for DataComplianceFilterSet."""

        model = DataCompliance
        fields = ["compliance_class_name", "validated_attribute", "content_type", "valid"]
