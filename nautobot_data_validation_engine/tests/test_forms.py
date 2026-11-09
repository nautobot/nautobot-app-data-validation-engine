"""Form test cases for nautobot_data_validation_engine."""

from nautobot.apps.testing import TestCase
from nautobot.dcim.models import Location, LocationType
from nautobot.extras.models import Status

from nautobot_data_validation_engine.forms import DataComplianceFilterForm
from nautobot_data_validation_engine.tests.test_data_compliance_rules import TestFailedDataComplianceRule


class DataComplianceFilterFormTestCase(TestCase):
    """Test cases for the DataComplianceFilterForm."""

    @classmethod
    def setUpTestData(cls):
        """Create DataCompliance records so the form has distinct values to offer."""
        location_type = LocationType(name="Region")
        location_type.validated_save()
        location = Location(
            name="Test Location 1",
            location_type=location_type,
            status=Status.objects.get_by_natural_key("Active"),
        )
        location.save()
        TestFailedDataComplianceRule(location).clean()

    def test_freetext_filters_offer_existing_values(self):
        """The compliance_class_name/validated_attribute dropdowns are seeded with existing values."""
        form = DataComplianceFilterForm()
        class_names = [value for value, _ in form.fields["compliance_class_name"].widget.choices]
        self.assertIn("TestFailedDataComplianceRule", class_names)
        attributes = [value for value, _ in form.fields["validated_attribute"].widget.choices]
        # TestFailedDataComplianceRule audits these attributes.
        self.assertIn("tenant", attributes)
        self.assertIn("name", attributes)
