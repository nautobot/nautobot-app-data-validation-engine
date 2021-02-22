"""
Django filters.
"""
import django_filters
from django.db.models import Q

from nautobot.extras.filters import CreatedUpdatedFilterSet
from nautobot.utilities.filters import BaseFilterSet, ContentTypeFilter

from nautobot_data_validation_engine.models import RegularExpressionValidationRule


class RegularExpressionValidationRuleFilterSet(BaseFilterSet, CreatedUpdatedFilterSet):
    """
    Base filterset for the RegularExpressionValidationRule model.
    """

    q = django_filters.CharFilter(
        method="search",
        label="Search",
    )
    content_type = ContentTypeFilter()

    class Meta:
        model = RegularExpressionValidationRule
        fields = ["id", "name", "regular_expression", "enabled", "content_type", "field", "error_message"]

    def search(self, queryset, name, value):
        """
        Custom filter method which searches a string value across several fields attached to the `q` filter field.
        """
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value)
            | Q(regular_expression__icontains=value)
            | Q(error_message__icontains=value)
            | Q(content_type__app_label=value)
            | Q(content_type__model=value)
            | Q(field=value)
        )
        return queryset.filter(qs_filter)
