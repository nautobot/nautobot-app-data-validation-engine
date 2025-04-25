"""Filtering for nautobot_data_validation_engine."""

from nautobot.apps.filters import NameSearchFilterSet, NautobotFilterSet

from nautobot_data_validation_engine import models


class ValidationRuleFilterSet(NameSearchFilterSet, NautobotFilterSet):  # pylint: disable=too-many-ancestors
    """Filter for ValidationRule."""

    class Meta:
        """Meta attributes for filter."""

        model = models.ValidationRule

        # add any fields from the model that you would like to filter your searches by using those
        fields = "__all__"
