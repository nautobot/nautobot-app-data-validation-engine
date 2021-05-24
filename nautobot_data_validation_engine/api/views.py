"""
API views
"""
from rest_framework.routers import APIRootView

from nautobot.core.api.views import ModelViewSet

from nautobot_data_validation_engine.api import serializers
from nautobot_data_validation_engine import models, filters


class DataValidationEngineRootView(APIRootView):
    """
    Data Validation Engine API root view
    """

    def get_view_name(self):
        return "Data Validation Engine"


class RegularExpressionValidationRuleViewSet(ModelViewSet):
    """
    View to manage regular expression validation rules
    """

    queryset = models.RegularExpressionValidationRule.objects.all()
    serializer_class = serializers.RegularExpressionValidationRuleSerializer
    filterset_class = filters.RegularExpressionValidationRuleFilterSet


class MinMaxValidationRuleViewSet(ModelViewSet):
    """
    View to manage min max expression validation rules
    """

    queryset = models.MinMaxValidationRule.objects.all()
    serializer_class = serializers.MinMaxValidationRuleSerializer
    filterset_class = filters.MinMaxValidationRuleFilterSet
