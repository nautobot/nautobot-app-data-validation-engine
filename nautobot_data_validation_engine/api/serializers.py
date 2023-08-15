"""API serializers."""

from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from nautobot.core.api import ContentTypeField
from nautobot.extras.api.serializers import NautobotModelSerializer
from nautobot.extras.api.mixins import TaggedModelSerializerMixin
from nautobot.extras.utils import FeatureQuery

from nautobot_data_validation_engine.models import (
    DataCompliance,
    MinMaxValidationRule,
    RegularExpressionValidationRule,
    RequiredValidationRule,
    UniqueValidationRule,
)


class RegularExpressionValidationRuleSerializer(NautobotModelSerializer, TaggedModelSerializerMixin):
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
            "content_type",
            "field",
            "regular_expression",
            "context_processing",
            "enabled",
            "error_message",
            "created",
            "last_updated",
            "tags",
        ]


class MinMaxValidationRuleSerializer(NautobotModelSerializer, TaggedModelSerializerMixin):
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
            "content_type",
            "field",
            "min",
            "max",
            "enabled",
            "error_message",
            "created",
            "last_updated",
            "tags",
        ]


class RequiredValidationRuleSerializer(NautobotModelSerializer, TaggedModelSerializerMixin):
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
            "content_type",
            "field",
            "enabled",
            "error_message",
            "created",
            "last_updated",
            "tags",
        ]


class UniqueValidationRuleSerializer(NautobotModelSerializer, TaggedModelSerializerMixin):
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
            "content_type",
            "field",
            "max_instances",
            "enabled",
            "error_message",
            "created",
            "last_updated",
            "tags",
        ]


class DataComplianceSerializer(NautobotModelSerializer):
    """Serializer for DataCompliance."""

    class Meta:
        """Meta class for serializer."""

        model = DataCompliance
        fields = "__all__"
