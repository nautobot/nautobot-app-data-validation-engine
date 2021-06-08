"""
View test cases
"""
from django.contrib.contenttypes.models import ContentType

from nautobot.dcim.models import Device, PowerFeed, Site
from nautobot.utilities.testing import ViewTestCases

from nautobot_data_validation_engine.models import MinMaxValidationRule, RegularExpressionValidationRule


class RegularExpressionValidationRuleTestCase(ViewTestCases.PrimaryObjectViewTestCase):
    """
    View test cases for the RegularExpressionValidationRule model
    """

    model = RegularExpressionValidationRule

    @classmethod
    def setUpTestData(cls):
        """
        Create test data
        """
        RegularExpressionValidationRule.objects.create(
            name="Regex rule 1",
            slug="regex-rule-1",
            content_type=ContentType.objects.get_for_model(Site),
            field="name",
            regular_expression="^.*$",
        )
        RegularExpressionValidationRule.objects.create(
            name="Regex rule 2",
            slug="regex-rule-2",
            content_type=ContentType.objects.get_for_model(Site),
            field="description",
            regular_expression="^.*$",
        )
        RegularExpressionValidationRule.objects.create(
            name="Regex rule 3",
            slug="regex-rule-3",
            content_type=ContentType.objects.get_for_model(Site),
            field="comments",
            regular_expression="^.*$",
        )

        cls.form_data = {
            "name": "Regex rule x",
            "slug": "regex-rule-x",
            "content_type": ContentType.objects.get_for_model(Site).pk,
            "field": "contact_name",
            "regular_expression": "^.*$",
        }

        cls.csv_data = (
            "name,slug,content_type,field,regular_expression",
            "Regex rule 4,regex-rule-4,dcim.site,contact_phone,^.*$",
            "Regex rule 5,regex-rule-5,dcim.site,physical_address,^.*$",
            "Regex rule 6,regex-rule-6,dcim.site,shipping_address,^.*$",
        )

        cls.bulk_edit_data = {
            "regular_expression": "^.*.*$",
            "enabled": False,
            "error_message": "no soup",
        }


class MinMaxValidationRuleTestCase(ViewTestCases.PrimaryObjectViewTestCase):
    """
    View test cases for the MinMaxValidationRule model
    """

    model = MinMaxValidationRule

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
        )
        MinMaxValidationRule.objects.create(
            name="Min max rule 2",
            slug="min-max-rule-2",
            content_type=ContentType.objects.get_for_model(PowerFeed),
            field="max_utilization",
            min=1,
        )
        MinMaxValidationRule.objects.create(
            name="Min max rule 3",
            slug="min-max-rule-3",
            content_type=ContentType.objects.get_for_model(PowerFeed),
            field="voltage",
            min=1,
        )

        cls.form_data = {
            "name": "Min max rule x",
            "slug": "min-max-rule-x",
            "content_type": ContentType.objects.get_for_model(Device).pk,
            "field": "position",
            "min": 5.0,
            "max": 6.0,
        }

        cls.csv_data = (
            "name,slug,content_type,field,min,max",
            "Min max rule 4,min-max-rule-4,dcim.device,vc_position,5,6",
            "Min max rule 5,min-max-rule-5,dcim.device,vc_priority,5,6",
            "Min max rule 6,min-max-rule-6,dcim.site,longitude,5,6",
        )

        cls.bulk_edit_data = {
            "min": 5.0,
            "max": 6.0,
            "enabled": False,
            "error_message": "no soup",
        }
