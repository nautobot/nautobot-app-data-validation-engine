"""Unit tests for nautobot_data_validation_engine."""

from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from nautobot.core.testing import APITestCase, APIViewTestCases
from nautobot.dcim.models import Location, LocationType, Manufacturer, Platform, PowerFeed
from nautobot.extras.models import Status

from nautobot_data_validation_engine.models import (
    MinMaxValidationRule,
    RegularExpressionValidationRule,
    RequiredValidationRule,
    UniqueValidationRule,
)
from nautobot_data_validation_engine.tests.test_data_compliance_rules import (
    TestFailedDataComplianceRule,
    TestPassedDataComplianceRule,
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
        response = self.client.get(f"{url}?format=api", **self.header)

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
        "url",
    ]
    choices_fields = {"content_type"}

    create_data = [
        {
            "name": "Regex rule 4",
            "content_type": "dcim.location",
            "field": "contact_name",
            "regular_expression": "^.*$",
        },
        {
            "name": "Regex rule 5",
            "content_type": "dcim.location",
            "field": "physical_address",
            "regular_expression": "^.*$",
        },
        {
            "name": "Regex rule 6",
            "content_type": "dcim.location",
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
            content_type=ContentType.objects.get_for_model(Location),
            field="name",
            regular_expression="^.*$",
        )
        RegularExpressionValidationRule.objects.create(
            name="Regex rule 2",
            content_type=ContentType.objects.get_for_model(Location),
            field="description",
            regular_expression="^.*$",
        )
        RegularExpressionValidationRule.objects.create(
            name="Regex rule 3",
            content_type=ContentType.objects.get_for_model(Location),
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
        "url",
    ]
    choices_fields = {"content_type"}

    create_data = [
        {
            "name": "Min max rule 4",
            "content_type": "dcim.device",
            "field": "vc_position",
            "min": 0,
            "max": 1,
        },
        {
            "name": "Min max rule 5",
            "content_type": "dcim.device",
            "field": "vc_priority",
            "min": -5.6,
            "max": 0,
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
            name="Min max rule 1",
            content_type=ContentType.objects.get_for_model(PowerFeed),
            field="amperage",
            min=1,
        )
        MinMaxValidationRule.objects.create(
            name="Min max rule 2",
            content_type=ContentType.objects.get_for_model(PowerFeed),
            field="max_utilization",
            min=1,
        )
        MinMaxValidationRule.objects.create(
            name="Min max rule 3",
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
        "url",
    ]
    choices_fields = {"content_type"}

    create_data = [
        {
            "name": "Required rule 4",
            "content_type": "dcim.location",
            "field": "physical_address",
        },
        {
            "name": "Required rule 5",
            "content_type": "dcim.location",
            "field": "asn",
        },
        {
            "name": "Required rule 6",
            "content_type": "dcim.location",
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
            content_type=ContentType.objects.get_for_model(Location),
            field="description",
        )
        RequiredValidationRule.objects.create(
            name="Required rule 2",
            content_type=ContentType.objects.get_for_model(Platform),
            field="description",
        )
        RequiredValidationRule.objects.create(
            name="Required rule 3",
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
        "url",
    ]
    choices_fields = {"content_type"}

    create_data = [
        {
            "name": "Unique rule 4",
            "content_type": "dcim.location",
            "field": "physical_address",
            "max_instances": 1,
        },
        {
            "name": "Unique rule 5",
            "content_type": "dcim.location",
            "field": "asn",
            "max_instances": 2,
        },
        {
            "name": "Unique rule 6",
            "content_type": "dcim.location",
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
            name="Unique rule 1",
            content_type=ContentType.objects.get_for_model(Location),
            field="description",
            max_instances=1,
        )
        UniqueValidationRule.objects.create(
            name="Unique rule 2",
            content_type=ContentType.objects.get_for_model(Platform),
            field="description",
            max_instances=2,
        )
        UniqueValidationRule.objects.create(
            name="Unique rule 3",
            content_type=ContentType.objects.get_for_model(Manufacturer),
            field="description",
            max_instances=3,
        )


class DataComplianceAPIFilterTest(APITestCase):
    """
    API filtering tests for the DataCompliance model.

    Regression coverage for the DataCompliance API view ignoring filter parameters because it had
    no ``filterset_class`` declared.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Create DataCompliance records against a real object so the generic foreign key resolves.

        ``TestFailedDataComplianceRule`` produces four ``valid=False`` records (one per audited
        attribute) and ``TestPassedDataComplianceRule`` produces a single ``valid=True`` record.
        """
        location_type = LocationType(name="Region")
        location_type.validated_save()
        location = Location(
            name="Test Location 1",
            location_type=location_type,
            status=Status.objects.get_by_natural_key("Active"),
        )
        location.save()
        TestFailedDataComplianceRule(location).clean()
        TestPassedDataComplianceRule(location).clean()

    def setUp(self):
        """Authenticate and grant view permission for the list endpoint."""
        super().setUp()
        self.add_permissions("nautobot_data_validation_engine.view_datacompliance")
        self.list_url = reverse("plugins-api:nautobot_data_validation_engine-api:datacompliance-list")

    def test_filter_valid(self):
        """The ``valid`` filter must be honored by the API."""
        response = self.client.get(f"{self.list_url}?valid=False", **self.header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 5)
        response = self.client.get(f"{self.list_url}?valid=True", **self.header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)

    def test_filter_content_type(self):
        """The ``content_type`` filter must be honored by the API."""
        response = self.client.get(f"{self.list_url}?content_type=dcim.location", **self.header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 6)

    def test_filter_compliance_class_name(self):
        """The ``compliance_class_name`` filter must be honored by the API."""
        response = self.client.get(f"{self.list_url}?compliance_class_name=TestFailedDataComplianceRule", **self.header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 5)
