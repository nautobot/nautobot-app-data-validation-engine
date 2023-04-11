from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from unittest.mock import MagicMock
from nautobot.dcim.models import Site
from nautobot_data_validation_engine.validations import ValidationSet
from nautobot_data_validation_engine.models import ValidationResult


class TestValidationSet(ValidationSet):
    model = "dcim.site"

    def validate_test_1(self, obj):
        self.success(obj, attribute="region", validated_attribute_value=obj.region)

    def validate_test_2(self, obj):
        self.fail(obj, attribute="tenant", validated_attribute_value=obj.tenant, message="Test Fail")

    def another_method(self, obj):
        self.success(obj, attribute="facility", validated_attribute_value=obj.facility)


class TestValidation(TestCase):
    def setUp(self):
        s = Site(name="Test 1")
        s.save()
        t = TestValidationSet()
        t.validate(job_result=MagicMock())

    def test_validate_only_runs_validate_methods(self):
        self.assertEqual(len(ValidationResult.objects.all()), 2)

    def test_validate_success(self):
        result = ValidationResult.objects.filter(valid=True).all()
        self.assertEqual(len(result), 1)
        result = result[0]
        self.assertEqual(result.class_name, "TestValidationSet")
        self.assertEqual(result.method_name, "validate_test_1")
        self.assertEqual(result.content_type, ContentType.objects.get_for_model(Site))
        self.assertEqual(result.object_id, str(Site.objects.first().id))
        self.assertEqual(result.validated_attribute, "region")
        self.assertEqual(result.validated_attribute_value, None)

    def test_validate_fail(self):
        result = ValidationResult.objects.filter(valid=False).all()
        self.assertEqual(len(result), 1)
        result = result[0]
        self.assertEqual(result.class_name, "TestValidationSet")
        self.assertEqual(result.method_name, "validate_test_2")
        self.assertEqual(result.content_type, ContentType.objects.get_for_model(Site))
        self.assertEqual(result.object_id, str(Site.objects.first().id))
        self.assertEqual(result.validated_attribute, "tenant")
        self.assertEqual(result.validated_attribute_value, None)

    def test_validate_replaces_results(self):
        t = TestValidationSet()
        self.assertEqual(len(ValidationResult.objects.all()), 2)
        t.validate(job_result=MagicMock())
        self.assertEqual(len(ValidationResult.objects.all()), 2)

    def test_validate_exception_if_not_in_validate_function(self):
        t = TestValidationSet()
        with self.assertRaises(Exception) as context:
            t.success(t)
        self.assertTrue("Unable to find calling method" in str(context.exception))
