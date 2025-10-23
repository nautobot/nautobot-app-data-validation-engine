"""API serializers for nautobot_data_validation_engine."""

from nautobot.apps.api import NautobotModelSerializer, TaggedModelSerializerMixin

from nautobot_data_validation_engine import models


class RegularExpressionValidationRuleSerializer(NautobotModelSerializer, TaggedModelSerializerMixin):  # pylint: disable=too-many-ancestors
    """RegularExpressionValidationRule Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.RegularExpressionValidationRule
        fields = "__all__"

        # Option for disabling write for certain fields:
        # read_only_fields = []
