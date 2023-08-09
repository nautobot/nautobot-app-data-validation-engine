"""
Model test cases
"""
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.test import TestCase

from nautobot.dcim.models import Location, Rack
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
            content_type=ContentType.objects.get_for_model(Location),
            field="name",
            regular_expression="^ABC$",
        )

        location = Location(name="does not match the regex", slug="location", status=Status.objects.get(slug="active"))

        with self.assertRaises(ValidationError):
            location.clean()

    def test_valid_regex_matches_do_not_raise_validation_error(self):
        RegularExpressionValidationRule.objects.create(
            name="Regex rule 1",
            slug="regex-rule-1",
            content_type=ContentType.objects.get_for_model(Location),
            field="name",
            regular_expression="^ABC$",
        )

        location = Location(name="ABC", slug="location", status=Status.objects.get(slug="active"))

        try:
            location.clean()
        except ValidationError as e:
            self.fail(f"rule.clean() failed validation: {e}")

    def test_empty_field_values_coerced_to_empty_string(self):
        RegularExpressionValidationRule.objects.create(
            name="Regex rule 1",
            slug="regex-rule-1",
            content_type=ContentType.objects.get_for_model(Location),
            field="description",
            regular_expression="^ABC$",
        )

        location = Location(
            name="does not match the regex",
            slug="location",
            description=None,  # empty value not allowed by the regex
            status=Status.objects.get(slug="active"),
        )

        with self.assertRaises(ValidationError):
            location.clean()

    def test_context_processing_happy_path(self):
        RegularExpressionValidationRule.objects.create(
            name="Regex rule 1",
            slug="regex-rule-1",
            content_type=ContentType.objects.get_for_model(Location),
            field="description",
            regular_expression="{{ object.name[0:3] }}.*",
            context_processing=True,
        )

        location = Location(
            name="AMS-195",
            slug="location",
            description="AMS-195 is really cool",  # This should match `AMS.*`
            status=Status.objects.get(slug="active"),
        )

        try:
            location.clean()
        except ValidationError as e:
            self.fail(f"rule.clean() failed validation: {e}")

    def test_context_processing_sad_path(self):
        RegularExpressionValidationRule.objects.create(
            name="Regex rule 1",
            slug="regex-rule-1",
            content_type=ContentType.objects.get_for_model(Location),
            field="description",
            regular_expression="{{ object.name[0:3] }}.*",
            context_processing=True,
        )

        location = Location(
            name="AMS-195",
            slug="location",
            description="I don't like AMS-195",  # This should *not* match `AMS.*`
            status=Status.objects.get(slug="active"),
        )

        with self.assertRaises(ValidationError):
            location.clean()

    def test_context_processing_invalid_regex_fails_validation(self):
        RegularExpressionValidationRule.objects.create(
            name="Regex rule 1",
            slug="regex-rule-1",
            content_type=ContentType.objects.get_for_model(Location),
            field="description",
            regular_expression="[{{ object.name[0:3] }}.*",  # once processed, this is an invalid regex
            context_processing=True,
        )

        location = Location(
            name="AMS-195",
            slug="location",
            status=Status.objects.get(slug="active"),
        )

        with self.assertRaises(ValidationError):
            location.clean()


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
            content_type=ContentType.objects.get_for_model(Location),
            field="latitude",
            min=1,
            max=1,
        )

        location = Location(
            name="does not match the regex",
            slug="location",
            latitude=None,  # empty value not allowed by the rule
            status=Status.objects.get(slug="active"),
        )

        with self.assertRaises(ValidationError):
            location.clean()

    def test_field_value_type_raise_validation_error(self):
        MinMaxValidationRule.objects.create(
            name="Min max rule 1",
            slug="min-max-rule-1",
            content_type=ContentType.objects.get_for_model(Location),
            field="latitude",
            min=1,
            max=1,
        )

        location = Location(
            name="does not match the regex",
            slug="location",
            latitude="foobar",  # wrong type
            status=Status.objects.get(slug="active"),
        )

        with self.assertRaises(ValidationError):
            location.clean()

    def test_min_violation_raise_validation_error(self):
        MinMaxValidationRule.objects.create(
            name="Min max rule 1",
            slug="min-max-rule-1",
            content_type=ContentType.objects.get_for_model(Location),
            field="latitude",
            min=5,
            max=10,
        )

        location = Location(
            name="does not match the regex",
            slug="location",
            latitude=4,  # less than min of 5
            status=Status.objects.get(slug="active"),
        )

        with self.assertRaises(ValidationError):
            location.clean()

    def test_max_violation_raise_validation_error(self):
        MinMaxValidationRule.objects.create(
            name="Min max rule 1",
            slug="min-max-rule-1",
            content_type=ContentType.objects.get_for_model(Location),
            field="latitude",
            min=5,
            max=10,
        )

        location = Location(
            name="does not match the regex",
            slug="location",
            latitude=11,  # more than max of 10
            status=Status.objects.get(slug="active"),
        )

        with self.assertRaises(ValidationError):
            location.clean()

    def test_unbounded_min_does_not_raise_validation_error(self):
        MinMaxValidationRule.objects.create(
            name="Min max rule 1",
            slug="min-max-rule-1",
            content_type=ContentType.objects.get_for_model(Location),
            field="latitude",
            min=None,  # unbounded
            max=10,
        )

        location = Location(
            name="does not match the regex",
            slug="location",
            latitude=-5,
            status=Status.objects.get(slug="active"),
        )

        try:
            location.clean()
        except ValidationError as e:
            self.fail(f"rule.clean() failed validation: {e}")

    def test_unbounded_max_does_not_raise_validation_error(self):
        MinMaxValidationRule.objects.create(
            name="Min max rule 1",
            slug="min-max-rule-1",
            content_type=ContentType.objects.get_for_model(Location),
            field="latitude",
            min=5,
            max=None,  # unbounded
        )

        location = Location(
            name="does not match the regex",
            slug="location",
            latitude=30,
            status=Status.objects.get(slug="active"),
        )

        try:
            location.clean()
        except ValidationError as e:
            self.fail(f"rule.clean() failed validation: {e}")

    def test_valid_bounded_value_does_not_raise_validation_error(self):
        MinMaxValidationRule.objects.create(
            name="Min max rule 1",
            slug="min-max-rule-1",
            content_type=ContentType.objects.get_for_model(Location),
            field="latitude",
            min=5,
            max=10,
        )

        location = Location(
            name="does not match the regex",
            slug="location",
            latitude=8,  # within bounds
            status=Status.objects.get(slug="active"),
        )

        try:
            location.clean()
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
            content_type=ContentType.objects.get_for_model(Location),
            field="description",
        )

        location = Location(
            name="Location 1 does not have a description", slug="location-1", status=Status.objects.get(slug="active")
        )

        with self.assertRaises(ValidationError):
            location.clean()

    def test_provided_values_no_not_raise_error(self):
        RequiredValidationRule.objects.create(
            name="Required rule 1",
            slug="required-rule-1",
            content_type=ContentType.objects.get_for_model(Location),
            field="description",
        )

        location = Location(
            name="Location 2 does have a description",
            slug="location-2",
            status=Status.objects.get(slug="active"),
            description="Location 2",
        )

        try:
            location.clean()
        except ValidationError as e:
            self.fail(f"rule.clean() failed validation: {e}")

    def test_empty_string_field_values_raise_error(self):
        RequiredValidationRule.objects.create(
            name="Required rule 3",
            slug="required-rule-3",
            content_type=ContentType.objects.get_for_model(Location),
            field="description",
        )

        location = Location(
            name="Location 3 has an empty string description",
            slug="location-3",
            status=Status.objects.get(slug="active"),
            description="",
        )

        with self.assertRaises(ValidationError):
            location.clean()

    def test_falsy_values_do_not_raise_error(self):
        RequiredValidationRule.objects.create(
            name="Required rule 4",
            slug="required-rule-4",
            content_type=ContentType.objects.get_for_model(Rack),
            field="serial",
        )

        location = Location(
            name="Location 3",
            slug="location-3",
            status=Status.objects.get(slug="active"),
        )
        location.save()

        rack = Rack(
            name="Rack 1",
            location=location,
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
            content_type=ContentType.objects.get_for_model(Location),
            field="asn",
            max_instances=1,
        )

        location1 = Location(name="Location 1", slug="location-1", status=Status.objects.get(slug="active"), asn=None)
        location2 = Location(name="Location 2", slug="location-2", status=Status.objects.get(slug="active"), asn=None)

        location1.validated_save()

        try:
            location2.clean()
        except ValidationError as e:
            self.fail(f"rule.clean() failed validation: {e}")

    def test_max_instances_reached_raises_error(self):
        UniqueValidationRule.objects.create(
            name="Unique rule 1",
            slug="unique-rule-1",
            content_type=ContentType.objects.get_for_model(Location),
            field="description",
            max_instances=2,
        )

        location1 = Location(
            name="Location 1", slug="location-1", status=Status.objects.get(slug="active"), asn=1, description="same"
        )
        location2 = Location(
            name="Location 2", slug="location-2", status=Status.objects.get(slug="active"), asn=2, description="same"
        )
        location3 = Location(
            name="Location 3", slug="location-3", status=Status.objects.get(slug="active"), asn=3, description="same"
        )

        location1.validated_save()
        location2.validated_save()

        with self.assertRaises(ValidationError):
            location3.clean()
