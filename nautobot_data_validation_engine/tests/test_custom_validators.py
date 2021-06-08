"""
Model test cases
"""
from django.contrib.contenttypes.models import ContentType
from django.core.validators import ValidationError
from django.test import TestCase

from nautobot.dcim.models import Site

from nautobot_data_validation_engine.models import MinMaxValidationRule, RegularExpressionValidationRule


class RegularExpressionValidationRuleModelTestCase(TestCase):
    """
    Test cases related to the RegularExpressionValidationRule model
    """

    def test_invalid_regex_matches_raise_validation_error(self):
        RegularExpressionValidationRule.objects.create(
            name="Regex rule 1",
            slug="regex-rule-1",
            content_type=ContentType.objects.get_for_model(Site),
            field="name",
            regular_expression="^ABC$",
        )

        site = Site(name="does not match the regex", slug="site")

        with self.assertRaises(ValidationError):
            site.clean()

    def test_valid_regex_matches_do_not_raise_validation_error(self):
        RegularExpressionValidationRule.objects.create(
            name="Regex rule 1",
            slug="regex-rule-1",
            content_type=ContentType.objects.get_for_model(Site),
            field="name",
            regular_expression="^ABC$",
        )

        site = Site(name="ABC", slug="site")

        try:
            site.clean()
        except ValidationError as e:
            self.fail(f"rule.clean() failed validation: {e}")

    def test_empty_field_values_coerced_to_empty_string(self):
        RegularExpressionValidationRule.objects.create(
            name="Regex rule 1",
            slug="regex-rule-1",
            content_type=ContentType.objects.get_for_model(Site),
            field="description",
            regular_expression="^ABC$",
        )

        site = Site(
            name="does not match the regex",
            slug="site",
            description=None,  # empty value not allowed by the regex
        )

        with self.assertRaises(ValidationError):
            site.clean()


class MinMaxValidationRuleModelTestCase(TestCase):
    """
    Test cases related to the MinMaxValidationRule model
    """

    def test_empty_field_values_raise_validation_error(self):
        MinMaxValidationRule.objects.create(
            name="Min max rule 1",
            slug="min-max-rule-1",
            content_type=ContentType.objects.get_for_model(Site),
            field="latitude",
            min=1,
            max=1,
        )

        site = Site(
            name="does not match the regex",
            slug="site",
            latitude=None,  # empty value not allowed by the rule
        )

        with self.assertRaises(ValidationError):
            site.clean()

    def test_field_value_type_raise_validation_error(self):
        MinMaxValidationRule.objects.create(
            name="Min max rule 1",
            slug="min-max-rule-1",
            content_type=ContentType.objects.get_for_model(Site),
            field="latitude",
            min=1,
            max=1,
        )

        site = Site(
            name="does not match the regex",
            slug="site",
            latitude="foobar",  # wrong type
        )

        with self.assertRaises(ValidationError):
            site.clean()

    def test_min_violation_raise_validation_error(self):
        MinMaxValidationRule.objects.create(
            name="Min max rule 1",
            slug="min-max-rule-1",
            content_type=ContentType.objects.get_for_model(Site),
            field="latitude",
            min=5,
            max=10,
        )

        site = Site(
            name="does not match the regex",
            slug="site",
            latitude=4,  # less than min of 5
        )

        with self.assertRaises(ValidationError):
            site.clean()

    def test_max_violation_raise_validation_error(self):
        MinMaxValidationRule.objects.create(
            name="Min max rule 1",
            slug="min-max-rule-1",
            content_type=ContentType.objects.get_for_model(Site),
            field="latitude",
            min=5,
            max=10,
        )

        site = Site(
            name="does not match the regex",
            slug="site",
            latitude=11,  # more than max of 10
        )

        with self.assertRaises(ValidationError):
            site.clean()

    def test_unbounded_min_does_not_raise_validation_error(self):
        MinMaxValidationRule.objects.create(
            name="Min max rule 1",
            slug="min-max-rule-1",
            content_type=ContentType.objects.get_for_model(Site),
            field="latitude",
            min=None,  # unbounded
            max=10,
        )

        site = Site(
            name="does not match the regex",
            slug="site",
            latitude=-5,
        )

        try:
            site.clean()
        except ValidationError as e:
            self.fail(f"rule.clean() failed validation: {e}")

    def test_unbounded_max_does_not_raise_validation_error(self):
        MinMaxValidationRule.objects.create(
            name="Min max rule 1",
            slug="min-max-rule-1",
            content_type=ContentType.objects.get_for_model(Site),
            field="latitude",
            min=5,
            max=None,  # unbounded
        )

        site = Site(
            name="does not match the regex",
            slug="site",
            latitude=30,
        )

        try:
            site.clean()
        except ValidationError as e:
            self.fail(f"rule.clean() failed validation: {e}")

    def test_valid_bounded_value_does_not_raise_validation_error(self):
        MinMaxValidationRule.objects.create(
            name="Min max rule 1",
            slug="min-max-rule-1",
            content_type=ContentType.objects.get_for_model(Site),
            field="latitude",
            min=5,
            max=10,
        )

        site = Site(
            name="does not match the regex",
            slug="site",
            latitude=8,  # within bounds
        )

        try:
            site.clean()
        except ValidationError as e:
            self.fail(f"rule.clean() failed validation: {e}")
