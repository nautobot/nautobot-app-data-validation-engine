"""DataComplianceRule test cases."""

from django.test import TestCase
from nautobot.dcim.models import Location, LocationType
from nautobot.extras.models import Status

from nautobot_data_validation_engine.custom_validators import ComplianceError, DataComplianceRule
from nautobot_data_validation_engine.models import DataCompliance


class TestFailedDataComplianceRule(DataComplianceRule):
    """Test implementation of DataComplianceRule."""

    model = "dcim.location"

    def audit(self):
        """Raises an AuditError."""
        # this should create 4 different Audits, one for each
        # attribute
        raise ComplianceError(
            {
                "tenant": "Tenant",
                "description": "Description",
                "name": "Name",
                "status": "Status",
            }
        )


class TestPassedDataComplianceRule(DataComplianceRule):
    """Test implementation of DataComplianceRule."""

    model = "dcim.location"

    def audit(self):
        """No exception means the audit passes."""


class TestCompliance(TestCase):
    """Test DataComplianceRule methods."""

    def setUp(self):
        self.location_type = LocationType(name="Region")
        self.location_type.save()
        self.s = Location(
            name="Test 1",
            location_type=LocationType.objects.get_by_natural_key("Region"),
            status=Status.objects.get_by_natural_key("Active"),
        )
        self.s.save()
        TestFailedDataComplianceRule(self.s).clean()
        TestPassedDataComplianceRule(self.s).clean()

    def test_audit_success(self):
        result = DataCompliance.objects.filter(valid=True).all()
        self.assertEqual(len(result), 1)
        result = result[0]
        self.assertEqual(result.compliance_class_name, "TestPassedDataComplianceRule")
        self.assertEqual(result.validated_object, self.s)
        self.assertEqual(result.validated_attribute, "__all__")
        self.assertEqual(result.validated_attribute_value, "")

    def test_audit_fail(self):
        result = DataCompliance.objects.filter(valid=False).all()
        self.assertEqual(len(result), 5)
        result = DataCompliance.objects.get(validated_attribute="tenant")
        self.assertEqual(result.compliance_class_name, "TestFailedDataComplianceRule")
        self.assertEqual(result.validated_object, self.s)
        self.assertIn(result.validated_attribute, "tenant")
        self.assertEqual(result.validated_attribute_value, "")

    def test_validate_replaces_results(self):
        self.assertEqual(
            len(DataCompliance.objects.filter(compliance_class_name=TestFailedDataComplianceRule.__name__)), 5
        )
        TestFailedDataComplianceRule(self.s).clean()
        self.assertEqual(
            len(DataCompliance.objects.filter(compliance_class_name=TestFailedDataComplianceRule.__name__)),
            5,
        )

    def test_custom_field_attribute_value(self):
        # Simulate a Location with a custom field value
        self.s.cf = {"foo": "bar"}
        # Patch DataComplianceRule.context to include our instance
        rule = TestPassedDataComplianceRule(self.s)
        rule.context = {"object": self.s}

        # Call _create_data_compliance_object with a custom field attribute
        obj = rule._create_data_compliance_object(attribute="cf_foo", valid=True, message="msg")
        self.assertEqual(obj.validated_attribute, "cf_foo")
        self.assertEqual(obj.validated_attribute_value, "bar")

    def test_custom_field_attribute_value_missing(self):
        # Simulate a Location with no custom field value
        self.s.cf = {}
        rule = TestPassedDataComplianceRule(self.s)
        rule.context = {"object": self.s}

        obj = rule._create_data_compliance_object(attribute="cf_missing", valid=True, message="msg")
        self.assertEqual(obj.validated_attribute, "cf_missing")
        self.assertIsNone(obj.validated_attribute_value)

    def test_regular_attribute_value(self):
        # Test with a regular attribute
        rule = TestPassedDataComplianceRule(self.s)
        rule.context = {"object": self.s}

        obj = rule._create_data_compliance_object(attribute="name", valid=True, message="msg")
        self.assertEqual(obj.validated_attribute, "name")
        self.assertEqual(obj.validated_attribute_value, self.s.name)
