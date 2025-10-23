"""API views for nautobot_data_validation_engine."""

from nautobot.apps.api import NautobotModelViewSet

from nautobot_data_validation_engine import filters, models
from nautobot_data_validation_engine.api import serializers


class RegularExpressionValidationRuleViewSet(NautobotModelViewSet):  # pylint: disable=too-many-ancestors
    """RegularExpressionValidationRule viewset."""

    queryset = models.RegularExpressionValidationRule.objects.all()
    serializer_class = serializers.RegularExpressionValidationRuleSerializer
    filterset_class = filters.RegularExpressionValidationRuleFilterSet

    # Option for modifying the default HTTP methods:
    # http_method_names = ["get", "post", "put", "patch", "delete", "head", "options", "trace"]
