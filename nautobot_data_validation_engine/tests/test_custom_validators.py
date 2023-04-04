"""
Model test cases
"""
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.test import TestCase

from nautobot.dcim.models import Site, Rack
from nautobot.extras.models import Status
from nautobot.extras.plugins.validators import wrap_model_clean_methods

from nautobot_data_validation_engine.models import (
    MinMaxValidationRule,
    RegularExpressionValidationRule,
    RequiredValidationRule,
    UniqueValidationRule,
)


class RegularExpressionValidationRuleModelTestCase(TestCase):
    """
    Test cases related to the RegularExpressionValidationRule model
    """

    def setUp(self) -> None:
        wrap_model_clean_methods()
        return super().setUp()

    def test_invalid_regex_matches_raise_validation_error(self):
        RegularExpressionValidationRule.objects.create(
            name="Regex rule 1",
            slug="regex-rule-1",
            content_type=ContentType.objects.get_for_model(Site),
            field="name",
            regular_expression="^ABC$",
        )

        site = Site(name="does not match the regex", slug="site", status=Status.objects.get(slug="active"))

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

        site = Site(name="ABC", slug="site", status=Status.objects.get(slug="active"))

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
            status=Status.objects.get(slug="active"),
        )

        with self.assertRaises(ValidationError):
            site.clean()

    def test_context_processing_happy_path(self):
        RegularExpressionValidationRule.objects.create(
            name="Regex rule 1",
            slug="regex-rule-1",
            content_type=ContentType.objects.get_for_model(Site),
            field="description",
            regular_expression="{{ object.name[0:3] }}.*",
            context_processing=True,
        )

        site = Site(
            name="AMS-195",
            slug="site",
            description="AMS-195 is really cool",  # This should match `AMS.*`
            status=Status.objects.get(slug="active"),
        )

        try:
            site.clean()
        except ValidationError as e:
            self.fail(f"rule.clean() failed validation: {e}")

    def test_context_processing_sad_path(self):
        RegularExpressionValidationRule.objects.create(
            name="Regex rule 1",
            slug="regex-rule-1",
            content_type=ContentType.objects.get_for_model(Site),
            field="description",
            regular_expression="{{ object.name[0:3] }}.*",
            context_processing=True,
        )

        site = Site(
            name="AMS-195",
            slug="site",
            description="I don't like AMS-195",  # This should *not* match `AMS.*`
            status=Status.objects.get(slug="active"),
        )

        with self.assertRaises(ValidationError):
            site.clean()

    def test_context_processing_invalid_regex_fails_validation(self):
        RegularExpressionValidationRule.objects.create(
            name="Regex rule 1",
            slug="regex-rule-1",
            content_type=ContentType.objects.get_for_model(Site),
            field="description",
            regular_expression="[{{ object.name[0:3] }}.*",  # once processed, this is an invalid regex
            context_processing=True,
        )

        site = Site(
            name="AMS-195",
            slug="site",
            status=Status.objects.get(slug="active"),
        )

        with self.assertRaises(ValidationError):
            site.clean()


class MinMaxValidationRuleModelTestCase(TestCase):
    """
    Test cases related to the MinMaxValidationRule model
    """

    def setUp(self) -> None:
        wrap_model_clean_methods()
        return super().setUp()

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
            status=Status.objects.get(slug="active"),
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
            status=Status.objects.get(slug="active"),
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
            status=Status.objects.get(slug="active"),
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
            status=Status.objects.get(slug="active"),
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
            status=Status.objects.get(slug="active"),
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
            status=Status.objects.get(slug="active"),
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
            status=Status.objects.get(slug="active"),
        )

        try:
            site.clean()
        except ValidationError as e:
            self.fail(f"rule.clean() failed validation: {e}")


class RequiredValidationRuleModelTestCase(TestCase):
    """
    Test cases related to the RequiredValidationRule model
    """

    def setUp(self) -> None:
        wrap_model_clean_methods()
        return super().setUp()

    def test_blank_value_raises_error(self):
        RequiredValidationRule.objects.create(
            name="Required rule 1",
            slug="required-rule-1",
            content_type=ContentType.objects.get_for_model(Site),
            field="description",
        )

        site = Site(name="Site 1 does not have a description", slug="site-1", status=Status.objects.get(slug="active"))

        with self.assertRaises(ValidationError):
            site.clean()

    def test_provided_values_no_not_raise_error(self):
        RequiredValidationRule.objects.create(
            name="Required rule 1",
            slug="required-rule-1",
            content_type=ContentType.objects.get_for_model(Site),
            field="description",
        )

        site = Site(
            name="Site 2 does have a description",
            slug="site-2",
            status=Status.objects.get(slug="active"),
            description="Site 2",
        )

        try:
            site.clean()
        except ValidationError as e:
            self.fail(f"rule.clean() failed validation: {e}")

    def test_empty_string_field_values_raise_error(self):
        RequiredValidationRule.objects.create(
            name="Required rule 3",
            slug="required-rule-3",
            content_type=ContentType.objects.get_for_model(Site),
            field="description",
        )

        site = Site(
            name="Site 3 has an empty string description",
            slug="site-3",
            status=Status.objects.get(slug="active"),
            description="",
        )

        with self.assertRaises(ValidationError):
            site.clean()

    def test_falsy_values_do_not_raise_error(self):
        RequiredValidationRule.objects.create(
            name="Required rule 4",
            slug="required-rule-4",
            content_type=ContentType.objects.get_for_model(Rack),
            field="serial",
        )

        site = Site(
            name="Site 3",
            slug="site-3",
            status=Status.objects.get(slug="active"),
        )
        site.save()

        rack = Rack(
            name="Rack 1",
            site=site,
            status=Status.objects.get(slug="active"),
            serial=0,  # test that zero passes validation
        )

        try:
            rack.clean()
        except ValidationError as e:
            self.fail(f"rule.clean() failed validation: {e}")


class UniqueValidationRuleModelTestCase(TestCase):
    """
    Test cases related to the UniqueValidationRule model
    """

    def setUp(self) -> None:
        wrap_model_clean_methods()
        return super().setUp()

    def test_blank_value_does_not_raise_error(self):
        UniqueValidationRule.objects.create(
            name="Unique rule 1",
            slug="unique-rule-1",
            content_type=ContentType.objects.get_for_model(Site),
            field="asn",
            max_instances=1,
        )

        site1 = Site(name="Site 1", slug="site-1", status=Status.objects.get(slug="active"), asn=None)
        site2 = Site(name="Site 2", slug="site-2", status=Status.objects.get(slug="active"), asn=None)

        site1.validated_save()

        try:
            site2.clean()
        except ValidationError as e:
            self.fail(f"rule.clean() failed validation: {e}")

    def test_max_instances_reached_raises_error(self):
        UniqueValidationRule.objects.create(
            name="Unique rule 1",
            slug="unique-rule-1",
            content_type=ContentType.objects.get_for_model(Site),
            field="description",
            max_instances=2,
        )

        site1 = Site(name="Site 1", slug="site-1", status=Status.objects.get(slug="active"), asn=1, description="same")
        site2 = Site(name="Site 2", slug="site-2", status=Status.objects.get(slug="active"), asn=2, description="same")
        site3 = Site(name="Site 3", slug="site-3", status=Status.objects.get(slug="active"), asn=3, description="same")

        site1.validated_save()
        site2.validated_save()

        with self.assertRaises(ValidationError):
            site3.clean()
