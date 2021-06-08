"""
API serializers
"""
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from nautobot.core.api import (
    ContentTypeField,
    ValidatedModelSerializer,
)
from nautobot.extras.utils import FeatureQuery

from nautobot_data_validation_engine.models import MinMaxValidationRule, RegularExpressionValidationRule


class RegularExpressionValidationRuleSerializer(ValidatedModelSerializer):
    """Serializer for `RegularExpressionValidationRule` objects."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:nautobot_data_validation_engine-api:regularexpressionvalidationrule-detail"
    )
    content_type = ContentTypeField(
        queryset=ContentType.objects.filter(FeatureQuery("custom_validators").get_query()),
    )

    class Meta:
        model = RegularExpressionValidationRule
        fields = [
            "id",
            "url",
            "name",
            "slug",
            "content_type",
            "field",
            "regular_expression",
            "enabled",
            "error_message",
            "created",
            "last_updated",
        ]


class MinMaxValidationRuleSerializer(ValidatedModelSerializer):
    """Serializer for `MinMaxValidationRule` objects."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:nautobot_data_validation_engine-api:minmaxvalidationrule-detail"
    )
    content_type = ContentTypeField(
        queryset=ContentType.objects.filter(FeatureQuery("custom_validators").get_query()),
    )

    class Meta:
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
