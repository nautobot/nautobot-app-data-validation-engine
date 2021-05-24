"""
API test cases
"""
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from nautobot.dcim.models import PowerFeed, Site
from nautobot.utilities.testing import APITestCase, APIViewTestCases

from nautobot_data_validation_engine.models import MinMaxValidationRule, RegularExpressionValidationRule


class AppTest(APITestCase):
    """
    Test base path for app
    """
    def test_root(self):
        """
        Test the root view
        """
        url = reverse("plugins-api:nautobot_data_validation_engine-api:api-root")
        response = self.client.get("{}?format=api".format(url), **self.header)

        self.assertEqual(response.status_code, 200)


class RegularExpressionValidationRuleTest(APIViewTestCases.APIViewTestCase):
    """
    API view test cases for the RegularExpressionValidationRule model
    """
    model = RegularExpressionValidationRule
    brief_fields = [
        "content_type",
        "created",
        "display",
        "enabled",
        "error_message",
        "field",
        "id",
        "last_updated",
        "name",
        "regular_expression",
        "url",
    ]

    create_data = [
        {
            "name": "Regex rule 4",
            "content_type": "dcim.site",
            "field": "contact_name",
            "regular_expression": "^.*$",
        },
        {
            "name": "Regex rule 5",
            "content_type": "dcim.site",
            "field": "physical_address",
            "regular_expression": "^.*$",
        },
        {
            "name": "Regex rule 6",
            "content_type": "dcim.site",
            "field": "shipping_address",
            "regular_expression": "^.*$",
        },
    ]
    bulk_update_data = {
        "enabled": False,
    }

    @classmethod
    def setUpTestData(cls):
        """
        Create test data
        """
        RegularExpressionValidationRule.objects.create(
            name="Regex rule 1",
            content_type=ContentType.objects.get_for_model(Site),
            field="name",
            regular_expression="^.*$",
        )
        RegularExpressionValidationRule.objects.create(
            name="Regex rule 2",
            content_type=ContentType.objects.get_for_model(Site),
            field="description",
            regular_expression="^.*$",
        )
        RegularExpressionValidationRule.objects.create(
            name="Regex rule 3",
            content_type=ContentType.objects.get_for_model(Site),
            field="comments",
            regular_expression="^.*$",
        )


class MinMaxValidationRuleTest(APIViewTestCases.APIViewTestCase):
    """
    API view test cases for the MinMaxValidationRule model
    """
    model = MinMaxValidationRule
    brief_fields = [
        "content_type",
        "created",
        "display",
        "enabled",
        "error_message",
        "field",
        "id",
        "last_updated",
        "max",
        "min",
        "name",
        "url",
    ]

    create_data = [
        {
            "name": "Min max rule 4",
            "content_type": "dcim.device",
            "field": "vc_position",
            "min": 5,
            "max": 6,
        },
        {
            "name": "Min max rule 5",
            "content_type": "dcim.device",
            "field": "vc_priority",
            "min": 5,
            "max": 6,
        },
        {
            "name": "Min max rule 6",
            "content_type": "dcim.device",
            "field": "position",
            "min": 5,
            "max": 6,
        },
    ]
    bulk_update_data = {
        "enabled": False,
    }

    @classmethod
    def setUpTestData(cls):
        """
        Create test data
        """
        MinMaxValidationRule.objects.create(
            name="Min max rule 1", content_type=ContentType.objects.get_for_model(PowerFeed), field="amperage", min=1
        )
        MinMaxValidationRule.objects.create(
            name="Min max rule 2",
            content_type=ContentType.objects.get_for_model(PowerFeed),
            field="max_utilization",
            min=1,
        )
        MinMaxValidationRule.objects.create(
            name="Min max rule 3", content_type=ContentType.objects.get_for_model(PowerFeed), field="voltage", min=1
        )
