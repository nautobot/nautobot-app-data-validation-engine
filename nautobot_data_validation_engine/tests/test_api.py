"""
API test cases
"""
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from nautobot.dcim.models import PowerFeed, Site, Region, Platform, Manufacturer
from nautobot.utilities.testing import APITestCase, APIViewTestCases

from nautobot_data_validation_engine.models import (
    MinMaxValidationRule,
    RegularExpressionValidationRule,
    RequiredValidationRule,
    UniqueValidationRule,
)


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
        "display",
        "id",
        "name",
        "slug",
        "url",
    ]

    create_data = [
        {
            "name": "Regex rule 4",
            "slug": "regex-rule-4",
            "content_type": "dcim.site",
            "field": "contact_name",
            "regular_expression": "^.*$",
        },
        {
            "name": "Regex rule 5",
            "slug": "regex-rule-5",
            "content_type": "dcim.site",
            "field": "physical_address",
            "regular_expression": "^.*$",
        },
        {
            "name": "Regex rule 6",
            "slug": "regex-rule-6",
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
            slug="regex-rule-1",
            content_type=ContentType.objects.get_for_model(Site),
            field="name",
            regular_expression="^.*$",
        )
        RegularExpressionValidationRule.objects.create(
            name="Regex rule 2",
            slug="regex-rule-2",
            content_type=ContentType.objects.get_for_model(Site),
            field="description",
            regular_expression="^.*$",
        )
        RegularExpressionValidationRule.objects.create(
            name="Regex rule 3",
            slug="regex-rule-3",
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
        "display",
        "id",
        "name",
        "slug",
        "url",
    ]

    create_data = [
        {
            "name": "Min max rule 4",
            "slug": "min-max-rule-4",
            "content_type": "dcim.device",
            "field": "vc_position",
            "min": 0,
            "max": 1,
        },
        {
            "name": "Min max rule 5",
            "slug": "min-max-rule-5",
            "content_type": "dcim.device",
            "field": "vc_priority",
            "min": -5.6,
            "max": 0,
        },
        {
            "name": "Min max rule 6",
            "slug": "min-max-rule-6",
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
            name="Min max rule 1",
            slug="min-max-rule-1",
            content_type=ContentType.objects.get_for_model(PowerFeed),
            field="amperage",
            min=1,
        )
        MinMaxValidationRule.objects.create(
            name="Min max rule 2",
            slug="min-max-rule-2",
            content_type=ContentType.objects.get_for_model(PowerFeed),
            field="max_utilization",
            min=1,
        )
        MinMaxValidationRule.objects.create(
            name="Min max rule 3",
            slug="min-max-rule-3",
            content_type=ContentType.objects.get_for_model(PowerFeed),
            field="voltage",
            min=1,
        )


class RequiredValidationRuleTest(APIViewTestCases.APIViewTestCase):
    """
    API view test cases for the RequiredValidationRule model
    """

    model = RequiredValidationRule
    brief_fields = [
        "display",
        "id",
        "name",
        "slug",
        "url",
    ]

    create_data = [
        {
            "name": "Required rule 4",
            "slug": "required-rule-4",
            "content_type": "dcim.site",
            "field": "description",
        },
        {
            "name": "Required rule 5",
            "slug": "required-rule-5",
            "content_type": "dcim.site",
            "field": "asn",
        },
        {
            "name": "Required rule 6",
            "slug": "required-rule-6",
            "content_type": "dcim.site",
            "field": "facility",
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
        RequiredValidationRule.objects.create(
            name="Required rule 1",
            slug="required-rule-1",
            content_type=ContentType.objects.get_for_model(Region),
            field="description",
        )
        RequiredValidationRule.objects.create(
            name="Required rule 2",
            slug="required-rule-2",
            content_type=ContentType.objects.get_for_model(Platform),
            field="description",
        )
        RequiredValidationRule.objects.create(
            name="Required rule 3",
            slug="required-rule-3",
            content_type=ContentType.objects.get_for_model(Manufacturer),
            field="description",
        )


class UniqueValidationRuleTest(APIViewTestCases.APIViewTestCase):
    """
    API view test cases for the UniqueValidationRule model
    """

    model = UniqueValidationRule
    brief_fields = [
        "display",
        "id",
        "name",
        "slug",
        "url",
    ]

    create_data = [
        {
            "name": "Required rule 4",
            "slug": "required-rule-4",
            "content_type": "dcim.site",
            "field": "description",
            "max_instances": 1,
        },
        {
            "name": "Required rule 5",
            "slug": "required-rule-5",
            "content_type": "dcim.site",
            "field": "asn",
            "max_instances": 2,
        },
        {
            "name": "Required rule 6",
            "slug": "required-rule-6",
            "content_type": "dcim.site",
            "field": "facility",
            "max_instances": 3,
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
        UniqueValidationRule.objects.create(
            name="Required rule 1",
            slug="required-rule-1",
            content_type=ContentType.objects.get_for_model(Region),
            field="description",
            max_instances=1,
        )
        UniqueValidationRule.objects.create(
            name="Required rule 2",
            slug="required-rule-2",
            content_type=ContentType.objects.get_for_model(Platform),
            field="description",
            max_instances=2,
        )
        UniqueValidationRule.objects.create(
            name="Required rule 3",
            slug="required-rule-3",
            content_type=ContentType.objects.get_for_model(Manufacturer),
            field="description",
            max_instances=3,
        )
