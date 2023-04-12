"""AuditRuleset test cases."""
from unittest.mock import MagicMock
from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from nautobot.dcim.models import Site
from nautobot_data_validation_engine.audit_rulesets import AuditRuleset
from nautobot_data_validation_engine.models import AuditRule


class TestAuditRuleset(AuditRuleset):
    """Test implementation of AuditRuleset."""

    model = "dcim.site"

    def audit_test_1(self, obj):
        """A method that runs via the AuditRuleset.audit method."""
        self.success(obj, attribute="region", validated_attribute_value=obj.region)

    def audit_test_2(self, obj):
        """A method that runs via the AuditRuleset.audit method."""
        self.fail(obj, attribute="tenant", validated_attribute_value=obj.tenant, message="Test Fail")

    def another_method(self, obj):
        """A method that should not be run via the AuditRuleset.validate method."""
        self.success(obj, attribute="facility", validated_attribute_value=obj.facility)


class TestValidation(TestCase):
    """Test AuditRuleset methods."""

    def setUp(self):
        s = Site(name="Test 1")
        s.save()
        t = TestAuditRuleset()
        t.audit(job_result=MagicMock())

    def test_audit_only_runs_audit_methods(self):
        self.assertEqual(len(AuditRule.objects.all()), 2)

    def test_audit_success(self):
        result = AuditRule.objects.filter(valid=True).all()
        self.assertEqual(len(result), 1)
        result = result[0]
        self.assertEqual(result.class_name, "TestAuditRuleset")
        self.assertEqual(result.method_name, "audit_test_1")
        self.assertEqual(result.content_type, ContentType.objects.get_for_model(Site))
        self.assertEqual(result.object_id, str(Site.objects.first().id))
        self.assertEqual(result.validated_attribute, "region")
        self.assertEqual(result.validated_attribute_value, None)

    def test_audit_fail(self):
        result = AuditRule.objects.filter(valid=False).all()
        self.assertEqual(len(result), 1)
        result = result[0]
        self.assertEqual(result.class_name, "TestAuditRuleset")
        self.assertEqual(result.method_name, "audit_test_2")
        self.assertEqual(result.content_type, ContentType.objects.get_for_model(Site))
        self.assertEqual(result.object_id, str(Site.objects.first().id))
        self.assertEqual(result.validated_attribute, "tenant")
        self.assertEqual(result.validated_attribute_value, None)

    def test_validate_replaces_results(self):
        t = TestAuditRuleset()
        self.assertEqual(len(AuditRule.objects.all()), 2)
        t.audit(job_result=MagicMock())
        self.assertEqual(len(AuditRule.objects.all()), 2)

    def test_validate_exception_if_not_in_validate_function(self):
        t = TestAuditRuleset()
        with self.assertRaises(Exception) as context:
            t.success(t)
        self.assertTrue("Unable to find calling method" in str(context.exception))
