"""Filtering for nautobot_data_validation_engine."""

import django_filters as filters
from django.db import models
from nautobot.apps.filters import NautobotFilterSet
from nautobot.core.filters import ContentTypeMultipleChoiceFilter, SearchFilter
from nautobot.extras.utils import FeatureQuery

from nautobot_data_validation_engine.models import (
    DataCompliance,
    MinMaxValidationRule,
    RegularExpressionValidationRule,
    RequiredValidationRule,
    UniqueValidationRule,
)


class ValidationRuleFilterSet(NameSearchFilterSet, NautobotFilterSet):  # pylint: disable=too-many-ancestors
    """Filter for ValidationRule."""

    class Meta:
        """Filterset metadata for the RegularExpressionValidationRule model."""

        model = RegularExpressionValidationRule
        fields = "__all__"

        # add any fields from the model that you would like to filter your searches by using those
        fields = "__all__"
