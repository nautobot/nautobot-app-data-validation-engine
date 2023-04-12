"""API serializers."""

from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from nautobot.core.api import ContentTypeField
from nautobot.extras.api.serializers import NautobotModelSerializer
from nautobot.extras.utils import FeatureQuery

from nautobot_data_validation_engine.models import (
    AuditRule,
    MinMaxValidationRule,
    RegularExpressionValidationRule,
    RequiredValidationRule,
    UniqueValidationRule,
)

# Not all of these variable(s) are not actually used anywhere in this file, but required for the
# automagically replacing a Serializer with its corresponding NestedSerializer.
from nautobot_data_validation_engine.api.nested_serializers import (  # noqa: F401
    NestedMinMaxValidationRuleSerializer,
    NestedRegularExpressionValidationRuleSerializer,
    NestedRequiredValidationRuleSerializer,
    NestedUniqueValidationRuleSerializer,
)


class RegularExpressionValidationRuleSerializer(NautobotModelSerializer):
    """Serializer for `RegularExpressionValidationRule` objects."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:nautobot_data_validation_engine-api:regularexpressionvalidationrule-detail"
    )
    content_type = ContentTypeField(
        queryset=ContentType.objects.filter(FeatureQuery("custom_validators").get_query()),
    )

    class Meta:
        """Serializer metadata for RegularExpressionValidationRule objects."""

        model = RegularExpressionValidationRule
        fields = [
            "id",
            "url",
            "name",
            "slug",
            "content_type",
            "field",
            "regular_expression",
            "context_processing",
            "enabled",
            "error_message",
            "created",
            "last_updated",
        ]


class MinMaxValidationRuleSerializer(NautobotModelSerializer):
    """Serializer for `MinMaxValidationRule` objects."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:nautobot_data_validation_engine-api:minmaxvalidationrule-detail"
    )
    content_type = ContentTypeField(
        queryset=ContentType.objects.filter(FeatureQuery("custom_validators").get_query()),
    )

    class Meta:
        """Serializer metadata for MinMaxValidationRule objects."""

        model = MinMaxValidationRule
        fields = [
            "id",
            "url",
            "name",
            "slug",
            "content_type",
            "field",
            "min",
            "max",
            "enabled",
            "error_message",
            "created",
            "last_updated",
        ]


class RequiredValidationRuleSerializer(NautobotModelSerializer):
    """Serializer for `RequiredValidationRule` objects."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:nautobot_data_validation_engine-api:requiredvalidationrule-detail"
    )
    content_type = ContentTypeField(
        queryset=ContentType.objects.filter(FeatureQuery("custom_validators").get_query()),
    )

    class Meta:
        """Serializer metadata for RequiredValidationRule objects."""

        model = RequiredValidationRule
        fields = [
            "id",
            "url",
            "name",
            "slug",
            "content_type",
            "field",
            "enabled",
            "error_message",
            "created",
            "last_updated",
        ]


class UniqueValidationRuleSerializer(NautobotModelSerializer):
    """Serializer for `UniqueValidationRule` objects."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:nautobot_data_validation_engine-api:uniquevalidationrule-detail"
    )
    content_type = ContentTypeField(
        queryset=ContentType.objects.filter(FeatureQuery("custom_validators").get_query()),
    )

    class Meta:
        """Serializer metadata for UniqueValidationRule objects."""

        model = UniqueValidationRule
        fields = [
            "id",
            "url",
            "name",
            "slug",
            "content_type",
            "field",
            "max_instances",
            "enabled",
            "error_message",
            "created",
            "last_updated",
        ]


class AuditRuleSerializer(NautobotModelSerializer):
    """Serializer for Validation Result."""

    class Meta:
        """Meta class for serializer."""

        model = AuditRule
        fields = "__all__"
