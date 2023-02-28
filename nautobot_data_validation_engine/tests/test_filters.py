"""
Filterset test cases
"""
from django.contrib.contenttypes.models import ContentType
from nautobot.utilities.testing.filters import FilterTestCases

from nautobot.dcim.models import PowerFeed, Rack, Region, Site, Platform, Manufacturer

from nautobot_data_validation_engine.filters import (
    MinMaxValidationRuleFilterSet,
    RegularExpressionValidationRuleFilterSet,
    RequiredValidationRuleFilterSet,
    UniqueValidationRuleFilterSet,
)
from nautobot_data_validation_engine.models import (
    MinMaxValidationRule,
    RegularExpressionValidationRule,
    RequiredValidationRule,
    UniqueValidationRule,
)


class RegularExpressionValidationRuleFilterTestCase(FilterTestCases.NameSlugFilterTestCase):
    """
    Filterset test cases for the RegularExpressionValidationRule model
    """

    queryset = RegularExpressionValidationRule.objects.all()
    filterset = RegularExpressionValidationRuleFilterSet

    @classmethod
    def setUpTestData(cls):
        """
        Create test data
        """
        RegularExpressionValidationRule.objects.create(
            name="Regex rule 1",
            slug="regex-rule-1",
            content_type=ContentType.objects.get_for_model(Rack),
            field="name",
            regular_expression="^ABC$",
            error_message="A",
        )
        RegularExpressionValidationRule.objects.create(
            name="Regex rule 2",
            slug="regex-rule-2",
            content_type=ContentType.objects.get_for_model(Region),
            field="description",
            regular_expression="DEF$",
            error_message="B",
        )
        RegularExpressionValidationRule.objects.create(
            name="Regex rule 3",
            slug="regex-rule-3",
            content_type=ContentType.objects.get_for_model(Site),
            field="comments",
            regular_expression="GHI",
            error_message="C",
        )

    def test_id(self):
        """Test ID lookups."""
        params = {"id": self.queryset.values_list("pk", flat=True)[:2]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_content_type(self):
        """Test content type lookups."""
        params = {"content_type": ["dcim.rack", "dcim.site"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_regular_expression(self):
        """Test regex lookups."""
        # TODO(john): revisit this once this is sorted: https://github.com/nautobot/nautobot/issues/477
        params = {"regular_expression": "^ABC$"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_error_message(self):
        """Test error message lookups."""
        params = {"error_message": ["A", "B"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_field(self):
        """Test field lookups."""
        params = {"field": ["name", "description"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)


class MinMaxValidationRuleFilterTestCase(FilterTestCases.NameSlugFilterTestCase):
    """
    Filterset test cases for the MinMaxValidationRule model
    """

    queryset = MinMaxValidationRule.objects.all()
    filterset = MinMaxValidationRuleFilterSet

    @classmethod
    def setUpTestData(cls):
        """
        Create test data
        """
        MinMaxValidationRule.objects.create(
            name="Min max rule 1",
            slug="min-max-rule-1",
            content_type=ContentType.objects.get_for_model(PowerFeed),
            field="amperage",
            min=1,
            error_message="A",
        )
        MinMaxValidationRule.objects.create(
            name="Min max rule 2",
            slug="min-max-rule-2",
            content_type=ContentType.objects.get_for_model(PowerFeed),
            field="max_utilization",
            min=1,
            error_message="B",
        )
        MinMaxValidationRule.objects.create(
            name="Min max rule 3",
            slug="min-max-rule-3",
            content_type=ContentType.objects.get_for_model(PowerFeed),
            field="voltage",
            min=1,
            error_message="C",
        )

    def test_id(self):
        """Test ID lookups."""
        params = {"id": self.queryset.values_list("pk", flat=True)[:2]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_content_type(self):
        """Test content type lookups."""
        params = {"content_type": ["dcim.powerfeed"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)

    def test_error_message(self):
        """Test error message lookups."""
        params = {"error_message": ["A", "B"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_field(self):
        """Test field lookups."""
        params = {"field": ["voltage", "max_utilization"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)


class RequiredValidationRuleFilterTestCase(FilterTestCases.NameSlugFilterTestCase):
    """
    Filterset test cases for the RequiredValidationRule model
    """

    queryset = RequiredValidationRule.objects.all()
    filterset = RequiredValidationRuleFilterSet

    @classmethod
    def setUpTestData(cls):
        """
        Create test data
        """
        RequiredValidationRule.objects.create(
            name="Required rule 1",
            slug="required-rule-1",
            content_type=ContentType.objects.get_for_model(Site),
            field="asn",
            error_message="A",
        )
        RequiredValidationRule.objects.create(
            name="Required rule 2",
            slug="required-rule-2",
            content_type=ContentType.objects.get_for_model(Platform),
            field="description",
            error_message="B",
        )
        RequiredValidationRule.objects.create(
            name="Required rule 3",
            slug="required-rule-3",
            content_type=ContentType.objects.get_for_model(Manufacturer),
            field="description",
            error_message="C",
        )

    def test_id(self):
        """Test ID lookups."""
        params = {"id": self.queryset.values_list("pk", flat=True)[:2]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_content_type(self):
        """Test content type lookups."""
        params = {"content_type": ["dcim.site"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_error_message(self):
        """Test error message lookups."""
        params = {"error_message": ["A", "B"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_field(self):
        """Test field lookups."""
        params = {"field": ["asn"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)


class UniqueValidationRuleFilterTestCase(FilterTestCases.NameSlugFilterTestCase):
    """
    Filterset test cases for the UniqueValidationRule model
    """

    queryset = UniqueValidationRule.objects.all()
    filterset = UniqueValidationRuleFilterSet

    @classmethod
    def setUpTestData(cls):
        """
        Create test data
        """
        UniqueValidationRule.objects.create(
            name="Unique rule 1",
            slug="unique-rule-1",
            content_type=ContentType.objects.get_for_model(Site),
            field="asn",
            max_instances=1,
            error_message="A",
        )
        UniqueValidationRule.objects.create(
            name="Unique rule 2",
            slug="unique-rule-2",
            content_type=ContentType.objects.get_for_model(Platform),
            field="description",
            max_instances=2,
            error_message="B",
        )
        UniqueValidationRule.objects.create(
            name="Unique rule 3",
            slug="unique-rule-3",
            content_type=ContentType.objects.get_for_model(Manufacturer),
            field="description",
            max_instances=3,
            error_message="C",
        )

    def test_id(self):
        """Test ID lookups."""
        params = {"id": self.queryset.values_list("pk", flat=True)[:2]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_content_type(self):
        """Test content type lookups."""
        params = {"content_type": ["dcim.site"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_error_message(self):
        """Test error message lookups."""
        params = {"error_message": ["A", "B"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_field(self):
        """Test field lookups."""
        params = {"field": ["asn"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_max_instances(self):
        """Test field lookups."""
        params = {"max_instances__gte": [2]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
