"""
Model test cases
"""
from django.contrib.contenttypes.models import ContentType
from django.core.validators import ValidationError
from django.test import TestCase

from nautobot.dcim.models import Cable, Device, PowerFeed
from nautobot.extras.models import Job

from nautobot_data_validation_engine.models import MinMaxValidationRule, RegularExpressionValidationRule


class RegularExpressionValidationRuleModelTestCase(TestCase):
    """
    Test cases related to the RegularExpressionValidationRule model
    """

    def test_invalid_field_name(self):
        """Test that a non-existent model field is rejected."""
        rule = RegularExpressionValidationRule.objects.create(
            name="Regex rule 1",
            slug="regex-rule-1",
            content_type=ContentType.objects.get_for_model(Device),
            field="afieldthatdoesnotexist",
            regular_expression="^.*$",
        )

        with self.assertRaises(ValidationError):
            rule.clean()

    def test_private_fields_cannot_be_used(self):
        """Test that a private model field is rejected."""
        rule = RegularExpressionValidationRule.objects.create(
            name="Regex rule 1",
            slug="regex-rule-1",
            content_type=ContentType.objects.get_for_model(Device),
            field="_name",  # _name is a private field
            regular_expression="^.*$",
        )

        with self.assertRaises(ValidationError):
            rule.clean()

    def test_non_editable_fields_cannot_be_used(self):
        """Test that a non-editable model field is rejected."""
        rule = RegularExpressionValidationRule.objects.create(
            name="Regex rule 1",
            slug="regex-rule-1",
            content_type=ContentType.objects.get_for_model(Device),
            field="created",  # created has auto_now_add=True, making it editable=False
            regular_expression="^.*$",
        )

        with self.assertRaises(ValidationError):
            rule.clean()

    def test_blacklisted_fields_cannot_be_used(self):
        """Test that a blacklisted model field is rejected."""
        rule = RegularExpressionValidationRule.objects.create(
            name="Regex rule 1",
            slug="regex-rule-1",
            content_type=ContentType.objects.get_for_model(Device),
            field="id",  # id is a uuid field which is blacklisted
            regular_expression="^.*$",
        )

        with self.assertRaises(ValidationError):
            rule.clean()

    def test_invalid_regex_fails_validation(self):
        """Test that an invalid regex string fails validation."""
        rule = RegularExpressionValidationRule.objects.create(
            name="Regex rule 1",
            slug="regex-rule-1",
            content_type=ContentType.objects.get_for_model(Device),
            field="name",
            regular_expression="[",  # this is an invalid regex pattern
        )

        with self.assertRaises(ValidationError):
            rule.full_clean()


class MinMaxValidationRuleModelTestCase(TestCase):
    """
    Test cases related to the MinMaxValidationRule model
    """

    def test_invalid_field_name(self):
        """Test that a non-existent model field is rejected."""
        rule = MinMaxValidationRule.objects.create(
            name="Min max rule 1",
            slug="min-max-rule-1",
            content_type=ContentType.objects.get_for_model(PowerFeed),
            field="afieldthatdoesnotexist",
            min=1,
        )

        with self.assertRaises(ValidationError):
            rule.clean()

    def test_private_fields_cannot_be_used(self):
        """Test that a private model field is rejected."""
        rule = MinMaxValidationRule.objects.create(
            name="Min max rule 1",
            slug="min-max-rule-1",
            content_type=ContentType.objects.get_for_model(Cable),
            field="_abs_length",  # this is a private field used for caching a denormalized value
            min=1,
        )

        with self.assertRaises(ValidationError):
            rule.clean()

    def test_blacklisted_fields_cannot_be_used(self):
        """Test that a blacklisted model field is rejected."""
        rule = MinMaxValidationRule.objects.create(
            name="Min max rule 1",
            slug="min-max-rule-1",
            content_type=ContentType.objects.get_for_model(Job),
            field="id",  # Job.id is an AutoField which is blacklisted
            min=1,
        )

        with self.assertRaises(ValidationError):
            rule.clean()

    def test_min_or_max_must_be_set(self):
        """Test that a blacklisted model field is rejected."""
        rule = MinMaxValidationRule.objects.create(
            name="Min max rule 1",
            slug="min-max-rule-1",
            content_type=ContentType.objects.get_for_model(PowerFeed),
            field="amperage",
        )

        with self.assertRaises(ValidationError):
            rule.clean()

    def test_min_must_be_less_than_max(self):
        """Test that a blacklisted model field is rejected."""
        rule = MinMaxValidationRule.objects.create(
            name="Min max rule 1",
            slug="min-max-rule-1",
            content_type=ContentType.objects.get_for_model(PowerFeed),
            field="amperage",
            min=1,
            max=0,
        )

        with self.assertRaises(ValidationError):
            rule.clean()

    def test_min__and_max_can_be_equal(self):
        """Test that a blacklisted model field is rejected."""
        rule = MinMaxValidationRule.objects.create(
            name="Min max rule 1",
            slug="min-max-rule-1",
            content_type=ContentType.objects.get_for_model(PowerFeed),
            field="amperage",
            min=1,
            max=1,
        )

        try:
            rule.clean()
        except ValidationError as e:
            self.fail(f"rule.clean() failed validation: {e}")
