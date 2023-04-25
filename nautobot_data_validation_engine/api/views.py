"""API views."""

from rest_framework.routers import APIRootView

from nautobot.extras.api.views import NautobotModelViewSet

from nautobot_data_validation_engine.api import serializers
from nautobot_data_validation_engine import models, filters


class DataValidationEngineRootView(APIRootView):
    """Data Validation Engine API root view."""

    def get_view_name(self):
        """Get the name of the view."""
        return "Data Validation Engine"


class RegularExpressionValidationRuleViewSet(NautobotModelViewSet):
    """View to manage regular expression validation rules."""

    queryset = models.RegularExpressionValidationRule.objects.all()
    serializer_class = serializers.RegularExpressionValidationRuleSerializer
    filterset_class = filters.RegularExpressionValidationRuleFilterSet


class MinMaxValidationRuleViewSet(NautobotModelViewSet):
    """View to manage min max expression validation rules."""

    queryset = models.MinMaxValidationRule.objects.all()
    serializer_class = serializers.MinMaxValidationRuleSerializer
    filterset_class = filters.MinMaxValidationRuleFilterSet


class RequiredValidationRuleViewSet(NautobotModelViewSet):
    """View to manage min max expression validation rules."""

    queryset = models.RequiredValidationRule.objects.all()
    serializer_class = serializers.RequiredValidationRuleSerializer
    filterset_class = filters.RequiredValidationRuleFilterSet


class UniqueValidationRuleViewSet(NautobotModelViewSet):
    """View to manage min max expression validation rules."""

    queryset = models.UniqueValidationRule.objects.all()
    serializer_class = serializers.UniqueValidationRuleSerializer
    filterset_class = filters.UniqueValidationRuleFilterSet


class AuditAPIView(NautobotModelViewSet):
    """API Views for Audit."""

    queryset = models.Audit.objects.all()
    serializer_class = serializers.AuditSerializer
