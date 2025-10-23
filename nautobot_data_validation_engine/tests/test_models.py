"""Test RegularExpressionValidationRule."""

from nautobot.apps.testing import ModelTestCases

from nautobot_data_validation_engine import models
from nautobot_data_validation_engine.tests import fixtures


class TestRegularExpressionValidationRule(ModelTestCases.BaseModelTestCase):
    """Test RegularExpressionValidationRule."""

    model = models.RegularExpressionValidationRule

    @classmethod
    def setUpTestData(cls):
        """Create test data for RegularExpressionValidationRule Model."""
        super().setUpTestData()
        # Create 3 objects for the model test cases.
        fixtures.create_regularexpressionvalidationrule()

    def test_create_regularexpressionvalidationrule_only_required(self):
        """Create with only required fields, and validate null description and __str__."""
        regularexpressionvalidationrule = models.RegularExpressionValidationRule.objects.create(name="Development")
        self.assertEqual(regularexpressionvalidationrule.name, "Development")
        self.assertEqual(regularexpressionvalidationrule.description, "")
        self.assertEqual(str(regularexpressionvalidationrule), "Development")

    def test_create_regularexpressionvalidationrule_all_fields_success(self):
        """Create RegularExpressionValidationRule with all fields."""
        regularexpressionvalidationrule = models.RegularExpressionValidationRule.objects.create(name="Development", description="Development Test")
        self.assertEqual(regularexpressionvalidationrule.name, "Development")
        self.assertEqual(regularexpressionvalidationrule.description, "Development Test")
