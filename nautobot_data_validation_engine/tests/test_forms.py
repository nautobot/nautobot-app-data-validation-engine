"""Test validationrule forms."""

from django.test import TestCase

from nautobot_data_validation_engine import forms


class ValidationRuleTest(TestCase):
    """Test ValidationRule forms."""

    def test_specifying_all_fields_success(self):
        form = forms.ValidationRuleForm(
            data={
                "name": "Development",
                "description": "Development Testing",
            }
        )
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def test_specifying_only_required_success(self):
        form = forms.ValidationRuleForm(
            data={
                "name": "Development",
            }
        )
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def test_validate_name_validationrule_is_required(self):
        form = forms.ValidationRuleForm(data={"description": "Development Testing"})
        self.assertFalse(form.is_valid())
        self.assertIn("This field is required.", form.errors["name"])
