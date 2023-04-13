"""Unit tests for nautobot_data_validation_engine views."""

from unittest import skipIf
from unittest.mock import MagicMock, patch
from packaging import version

from django.contrib.contenttypes.models import ContentType
from django.http.request import QueryDict
from nautobot.dcim.models import Device, PowerFeed, Site
from nautobot.utilities.testing import ViewTestCases, TestCase

from nautobot_data_validation_engine.models import (
    MinMaxValidationRule,
    RegularExpressionValidationRule,
    RequiredValidationRule,
    UniqueValidationRule,
    AuditResult,
)
from nautobot_data_validation_engine.tests.test_audit_rulesets import TestAuditRuleset
from nautobot_data_validation_engine.views import AuditResultObjectView
from nautobot_data_validation_engine.tables import AuditResultTableTab

try:
    from importlib import metadata
except ImportError:
    # Running on pre-3.8 Python; use importlib-metadata package
    import importlib_metadata as metadata

_NAUTOBOT_VERSION = version.parse(metadata.version("nautobot"))
# Related to this issue: https://github.com/nautobot/nautobot/issues/2948
_FAILING_OBJECT_LIST_NAUTOBOT_VERSIONS = [version.parse("1.5.2"), version.parse("1.5.3"), version.parse("1.5.4")]


class RegularExpressionValidationRuleTestCase(ViewTestCases.PrimaryObjectViewTestCase):
    """View test cases for the RegularExpressionValidationRule model."""

    model = RegularExpressionValidationRule

    @skipIf(
        _NAUTOBOT_VERSION in _FAILING_OBJECT_LIST_NAUTOBOT_VERSIONS,
        f"Skip test in Nautobot version {_NAUTOBOT_VERSION} due to Nautobot issue #2948",
    )
    def test_list_objects_with_permission(self):
        super().test_list_objects_with_permission()

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
    """View test cases for the MinMaxValidationRule model."""

    model = MinMaxValidationRule

    @skipIf(
        _NAUTOBOT_VERSION in _FAILING_OBJECT_LIST_NAUTOBOT_VERSIONS,
        f"Skip test in Nautobot version {_NAUTOBOT_VERSION} due to Nautobot issue #2948",
    )
    def test_list_objects_with_permission(self):
        super().test_list_objects_with_permission()

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


class RequiredValidationRuleTestCase(ViewTestCases.PrimaryObjectViewTestCase):
    """View test cases for the RequiredValidationRule model."""

    model = RequiredValidationRule

    @skipIf(
        _NAUTOBOT_VERSION in _FAILING_OBJECT_LIST_NAUTOBOT_VERSIONS,
        f"Skip test in Nautobot version {_NAUTOBOT_VERSION} due to Nautobot issue #2948",
    )
    def test_list_objects_with_permission(self):
        super().test_list_objects_with_permission()

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
        )
        RequiredValidationRule.objects.create(
            name="Required rule 2",
            slug="required-rule-2",
            content_type=ContentType.objects.get_for_model(Site),
            field="description",
        )
        RequiredValidationRule.objects.create(
            name="Required rule 3",
            slug="required-rule-3",
            content_type=ContentType.objects.get_for_model(Site),
            field="comments",
        )

        cls.form_data = {
            "name": "Required rule x",
            "slug": "required-rule-x",
            "content_type": ContentType.objects.get_for_model(Site).pk,
            "field": "contact_name",
        }

        cls.csv_data = (
            "name,slug,content_type,field",
            "Required rule 4,required-rule-4,dcim.site,contact_phone",
            "Required rule 5,required-rule-5,dcim.site,physical_address",
            "Required rule 6,required-rule-6,dcim.site,shipping_address",
        )

        cls.bulk_edit_data = {
            "enabled": False,
            "error_message": "no soup",
        }


class UniqueValidationRuleTestCase(ViewTestCases.PrimaryObjectViewTestCase):
    """View test cases for the UniqueValidationRule model."""

    model = UniqueValidationRule

    @skipIf(
        _NAUTOBOT_VERSION in _FAILING_OBJECT_LIST_NAUTOBOT_VERSIONS,
        f"Skip test in Nautobot version {_NAUTOBOT_VERSION} due to Nautobot issue #2948",
    )
    def test_list_objects_with_permission(self):
        super().test_list_objects_with_permission()

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
        )
        UniqueValidationRule.objects.create(
            name="Unique rule 2",
            slug="unique-rule-2",
            content_type=ContentType.objects.get_for_model(Site),
            field="description",
            max_instances=2,
        )
        UniqueValidationRule.objects.create(
            name="Unique rule 3",
            slug="unique-rule-3",
            content_type=ContentType.objects.get_for_model(Site),
            field="comments",
            max_instances=3,
        )

        cls.form_data = {
            "name": "Unique rule x",
            "slug": "unique-rule-x",
            "content_type": ContentType.objects.get_for_model(Site).pk,
            "field": "contact_name",
            "max_instances": 4,
        }

        cls.csv_data = (
            "name,slug,content_type,field,max_instances",
            "Unique rule 4,unique-rule-4,dcim.site,contact_phone,1",
            "Unique rule 5,unique-rule-5,dcim.site,physical_address,2",
            "Unique rule 6,unique-rule-6,dcim.site,shipping_address,3",
        )

        cls.bulk_edit_data = {
            "max_instances": 4,
            "enabled": False,
            "error_message": "no soup",
        }


class AuditRuleTestCase(
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    """Test cases for AuditResult Viewset."""

    model = AuditResult

    @skipIf(
        _NAUTOBOT_VERSION in _FAILING_OBJECT_LIST_NAUTOBOT_VERSIONS,
        f"Skip test in Nautobot version {_NAUTOBOT_VERSION} due to Nautobot issue #2948",
    )
    def test_list_objects_with_permission(self):
        super().test_list_objects_with_permission()

    @classmethod
    def setUpTestData(cls):
        s = Site(name="Test Site 1")
        s.save()
        t = TestAuditRuleset()
        t.audit(job_result=MagicMock())


class AuditResultObjectTestCase(TestCase):
    """Test cases for AuditResultObjectView."""

    def setUp(self):
        s = Site(name="Test Site 1")
        s.save()
        t = TestAuditRuleset()
        t.audit(job_result=MagicMock())

    def test_get_extra_context(self):
        view = AuditResultObjectView()
        site = Site.objects.first()
        mock_request = MagicMock()
        mock_request.GET = QueryDict("tab=nautobot_data_validation_engine:1")
        result = view.get_extra_context(mock_request, site)
        self.assertEqual(result["active_tab"], "nautobot_data_validation_engine:1")
        self.assertIsInstance(result["table"], AuditResultTableTab)

    @patch("nautobot.core.views.generic.ObjectView.dispatch")
    def test_dispatch(self, mocked_dispatch):  # pylint: disable=R0201
        view = AuditResultObjectView()
        mock_request = MagicMock()
        kwargs = {"model": "dcim.site", "other_arg": "other_arg", "another_arg": "another_arg"}
        view.dispatch(mock_request, **kwargs)
        mocked_dispatch.assert_called()
        mocked_dispatch.assert_called_with(mock_request, other_arg="other_arg", another_arg="another_arg")
