"""API serializers."""

from rest_framework import serializers

from nautobot.core.api import WritableNestedSerializer

from nautobot_data_validation_engine.models import (
    MinMaxValidationRule,
    RegularExpressionValidationRule,
    RequiredValidationRule,
    UniqueValidationRule,
)


__all__ = [
    "NestedRegularExpressionValidationRuleSerializer",
    "NestedMinMaxValidationRuleSerializer",
    "NestedRequiredValidationRuleSerializer",
    "NestedUniqueValidationRuleSerializer",
]


class NestedRegularExpressionValidationRuleSerializer(WritableNestedSerializer):
    """Serializer for `RegularExpressionValidationRule` objects."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:nautobot_data_validation_engine-api:regularexpressionvalidationrule-detail"
    )

    class Meta:
        """Serializer metadata for RegularExpressionValidationRule objects."""

        model = RegularExpressionValidationRule
        fields = [
            "id",
            "url",
            "name",
            "slug",
        ]


class NestedMinMaxValidationRuleSerializer(WritableNestedSerializer):
    """Serializer for `MinMaxValidationRule` objects."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:nautobot_data_validation_engine-api:minmaxvalidationrule-detail"
    )

    class Meta:
        """Serializer metadata for MinMaxValidationRule objects."""

        model = MinMaxValidationRule
        fields = [
            "id",
            "url",
            "name",
            "slug",
        ]


class NestedRequiredValidationRuleSerializer(WritableNestedSerializer):
    """Serializer for `RequiredValidationRule` objects."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:nautobot_data_validation_engine-api:requiredvalidationrule-detail"
    )

    class Meta:
        """Serializer metadata for RequiredValidationRule objects."""

        model = RequiredValidationRule
        fields = [
            "id",
            "url",
            "name",
            "slug",
        ]


class NestedUniqueValidationRuleSerializer(WritableNestedSerializer):
    """Serializer for `UniqueValidationRule` objects."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:nautobot_data_validation_engine-api:uniquevalidationrule-detail"
    )

    class Meta:
        """Serializer metadata for UniqueValidationRule objects."""

        model = UniqueValidationRule
        fields = [
            "id",
            "url",
            "name",
            "slug",
        ]
