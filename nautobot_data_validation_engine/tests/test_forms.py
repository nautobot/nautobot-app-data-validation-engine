"""Test regularexpressionvalidationrule forms."""

from django.test import TestCase

from nautobot_data_validation_engine import forms


class RegularExpressionValidationRuleTest(TestCase):
    """Test RegularExpressionValidationRule forms."""

    def test_specifying_all_fields_success(self):
        form = forms.RegularExpressionValidationRuleForm(
            data={
                "name": "Development",
                "description": "Development Testing",
            }
        )
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def test_specifying_only_required_success(self):
        form = forms.RegularExpressionValidationRuleForm(
            data={
                "name": "Development",
            }
        )
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def test_validate_name_regularexpressionvalidationrule_is_required(self):
        form = forms.RegularExpressionValidationRuleForm(data={"description": "Development Testing"})
        self.assertFalse(form.is_valid())
        self.assertIn("This field is required.", form.errors["name"])
