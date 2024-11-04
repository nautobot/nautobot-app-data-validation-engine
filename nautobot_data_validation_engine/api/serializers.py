"""API serializers."""

from django.contrib.contenttypes.models import ContentType
from nautobot.core.api import ContentTypeField
from nautobot.extras.api.mixins import TaggedModelSerializerMixin
from nautobot.extras.api.serializers import NautobotModelSerializer
from nautobot.extras.utils import FeatureQuery
from rest_framework import serializers

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
        fields = "__all__"


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
        fields = "__all__"


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
        fields = "__all__"


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
        fields = "__all__"


class DataComplianceSerializer(NautobotModelSerializer):
    """Serializer for DataCompliance."""

    class Meta:
        """Meta class for serializer."""

        model = DataCompliance
        fields = "__all__"
