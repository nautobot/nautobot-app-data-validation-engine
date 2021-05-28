"""
Django filters.
"""
import django_filters
from django.db.models import Q

from nautobot.extras.filters import CreatedUpdatedFilterSet
from nautobot.extras.utils import FeatureQuery
from nautobot.utilities.filters import BaseFilterSet, ContentTypeMultipleChoiceFilter

from nautobot_data_validation_engine.models import MinMaxValidationRule, RegularExpressionValidationRule


class RegularExpressionValidationRuleFilterSet(BaseFilterSet, CreatedUpdatedFilterSet):
    """
    Base filterset for the RegularExpressionValidationRule model.
    """

    q = django_filters.CharFilter(
        method="search",
        label="Search",
    )
    content_type = ContentTypeMultipleChoiceFilter(
        choices=FeatureQuery("custom_validators").get_choices, conjoined=False  # Make this an OR with multi-values
    )

    class Meta:
        model = RegularExpressionValidationRule
        fields = ["id", "name", "slug", "regular_expression", "enabled", "content_type", "field", "error_message"]

    def search(self, queryset, name, value):
        """
        Custom filter method which searches a string value across several fields attached to the `q` filter field.
        """
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value)
            | Q(slug__icontains=value)
            | Q(regular_expression__icontains=value)
            | Q(error_message__icontains=value)
            | Q(content_type__app_label=value)
            | Q(content_type__model=value)
            | Q(field=value)
        )
        return queryset.filter(qs_filter)


class MinMaxValidationRuleFilterSet(BaseFilterSet, CreatedUpdatedFilterSet):
    """
    Base filterset for the MinMaxValidationRule model.
    """

    q = django_filters.CharFilter(
        method="search",
        label="Search",
    )
    content_type = ContentTypeMultipleChoiceFilter(
        choices=FeatureQuery("custom_validators").get_choices, conjoined=False  # Make this an OR with multi-values
    )

    class Meta:
        model = MinMaxValidationRule
        fields = ["id", "name", "slug", "min", "max", "enabled", "content_type", "field", "error_message"]

    def search(self, queryset, name, value):
        """
        Custom filter method which searches a string value across several fields attached to the `q` filter field.
        """
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value)
            | Q(slug__icontains=value)
            | Q(error_message__icontains=value)
            | Q(content_type__app_label=value)
            | Q(content_type__model=value)
            | Q(field=value)
        )
        return queryset.filter(qs_filter)
