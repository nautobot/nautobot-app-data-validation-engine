"""AuditRuleset test cases."""
from django.test import TestCase
from nautobot.dcim.models import Site
from nautobot_data_validation_engine.custom_validators import AuditError, AuditRuleset
from nautobot_data_validation_engine.models import AuditResult


class TestFailedAuditRuleset(AuditRuleset):
    """Test implementation of AuditRuleset."""

    model = "dcim.site"

    def audit(self):  # pylint: disable=R0201
        """Raises an AuditError."""
        # this should create 4 different AuditResults, one for each
        # attribute
        raise AuditError(
            {
                "tenant": "Tenant",
                "region": "Region",
                "name": "Name",
                "status": "Status",
            }
        )


class TestPassedAuditRuleset(AuditRuleset):
    """Test implementation of AuditRuleset."""

    model = "dcim.site"

    def audit(self):
        """No exception means the audit passes."""


class TestValidation(TestCase):
    """Test AuditRuleset methods."""

    def setUp(self):
        self.s = Site(name="Test 1")
        self.s.save()
        TestFailedAuditRuleset(self.s).clean()
        TestPassedAuditRuleset(self.s).clean()

    def test_audit_success(self):
        result = AuditResult.objects.filter(valid=True).all()
        self.assertEqual(len(result), 1)
        result = result[0]
        self.assertEqual(result.audit_class_name, "TestPassedAuditRuleset")
        self.assertEqual(result.validated_object, self.s)
        self.assertEqual(result.validated_attribute, "all")
        self.assertEqual(result.validated_attribute_value, None)

    def test_audit_fail(self):
        result = AuditResult.objects.filter(valid=False).all()
        self.assertEqual(len(result), 5)
        result = result[0]
        self.assertEqual(result.audit_class_name, "TestFailedAuditRuleset")
        self.assertEqual(result.validated_object, self.s)
        self.assertEqual(result.validated_attribute, "tenant")
        self.assertEqual(result.validated_attribute_value, None)

    def test_validate_replaces_results(self):
        self.assertEqual(len(AuditResult.objects.filter(audit_class_name=TestFailedAuditRuleset.__name__)), 5)
        TestFailedAuditRuleset(self.s).clean()
        self.assertEqual(len(AuditResult.objects.filter(audit_class_name=TestFailedAuditRuleset.__name__)), 5)
