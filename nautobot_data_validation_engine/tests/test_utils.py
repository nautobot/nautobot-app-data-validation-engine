"""Tests for the regular expression helpers."""

from types import SimpleNamespace

import regex
from django.conf import settings
from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings
from jinja2.exceptions import SecurityError

from nautobot_data_validation_engine.utils import (
    REGEX_TIMEOUT_DEFAULT,
    InvalidRegexError,
    RegexTimeoutError,
    regex_match,
    render_jinja2_for_regex,
)

# Wide alternation rather than a nested quantifier: the `regex` module optimizes the classic
# `((((a*)*)*)*)*` form away, but backtracks catastrophically on this one. The trailing "X" prevents
# `$` from ever matching, forcing the engine to try every partition of the leading "a" run.
REDOS_PATTERN = "(a|a|a|a|a)+$"
REDOS_SUBJECT = "a" * 20 + "X"


class RegexMatchTestCase(TestCase):
    """Tests for the timeout-bounded `regex_match()` helper."""

    def test_regex_match_is_anchored_at_start_of_value(self):
        self.assertIsNotNone(regex_match("a+", "aaabbb"))
        self.assertIsNone(regex_match("b+", "aaabbb"))

    def test_uncompilable_pattern_raises_invalid_regex_error(self):
        with self.assertRaises(InvalidRegexError) as context:
            regex_match("(", "anything")
        # A ValidationError subclass so that a caller which does not catch it still fails closed.
        self.assertIsInstance(context.exception, ValidationError)
        self.assertEqual(context.exception.code, "regex_invalid")

    def test_catastrophic_pattern_raises_regex_timeout_error(self):
        with self.assertRaises(RegexTimeoutError) as context:
            regex_match(REDOS_PATTERN, REDOS_SUBJECT, timeout=0.1)
        self.assertIsInstance(context.exception, ValidationError)
        self.assertEqual(context.exception.code, "regex_timeout")
        self.assertIn("catastrophic backtracking", context.exception.messages[0])

    @override_settings(REGEX_TIMEOUT=0.05)
    def test_configured_timeout_applies_when_not_passed_explicitly(self):
        with self.assertRaises(RegexTimeoutError) as context:
            regex_match(REDOS_PATTERN, REDOS_SUBJECT)
        self.assertIn("exceeded 0.05 second(s)", context.exception.messages[0])

    @override_settings()
    def test_default_timeout_applies_when_nautobot_has_no_setting(self):
        """Nautobot releases before `REGEX_TIMEOUT` was added must still get a bounded match."""
        del settings.REGEX_TIMEOUT
        with self.assertRaises(RegexTimeoutError) as context:
            regex_match(REDOS_PATTERN, REDOS_SUBJECT)
        self.assertIn(f"exceeded {REGEX_TIMEOUT_DEFAULT} second(s)", context.exception.messages[0])

    def test_timeout_is_logged_with_the_offending_pattern(self):
        # Operators need to be able to find which stored pattern is responsible.
        with self.assertLogs("nautobot_data_validation_engine.utils", level="ERROR") as logs:
            with self.assertRaises(RegexTimeoutError):
                regex_match(REDOS_PATTERN, REDOS_SUBJECT, timeout=0.1)
        self.assertIn(REDOS_PATTERN, logs.output[0])


class RenderJinja2ForRegexTestCase(TestCase):
    """Tests for rendering a Jinja2 template whose output is used as a regular expression."""

    def test_interpolated_metacharacters_are_escaped(self):
        rendered = render_jinja2_for_regex("^{{ v }}$", {"v": "a.b"})
        self.assertEqual(rendered, r"^a\.b$")

    def test_literal_template_text_is_not_escaped(self):
        """The template author keeps full control of the pattern's own syntax."""
        self.assertEqual(render_jinja2_for_regex("^[a-z]+$", {}), "^[a-z]+$")

    def test_interpolated_value_cannot_change_the_pattern_structure(self):
        """A value of `.*` must become a literal, not a wildcard that defeats the rule."""
        rendered = render_jinja2_for_regex("^{{ v }}$", {"v": ".*"})
        self.assertEqual(rendered, r"^\.\*$")
        self.assertIsNone(regex.match(rendered, "anything else"))

    def test_interpolated_value_is_not_html_escaped(self):
        rendered = render_jinja2_for_regex("^{{ v }}$", {"v": "a&b"})
        self.assertIsNotNone(regex.match(rendered, "a&b"))

    def test_escaping_applies_through_filters_and_safe(self):
        for template_code, expected in [
            ("{{ v|safe }}", r"a\.b"),
            ("{{ v|upper }}", r"A\.B"),
            ("{% set x = v %}{{ x }}", r"a\.b"),
        ]:
            with self.subTest(template_code=template_code):
                self.assertEqual(render_jinja2_for_regex(template_code, {"v": "a.b"}), expected)

    def test_non_string_values_are_coerced(self):
        self.assertEqual(render_jinja2_for_regex("{{ v }}", {"v": 42}), "42")

    def test_undefined_variables_render_empty(self):
        self.assertEqual(render_jinja2_for_regex("{{ nope }}", {}), "")

    def test_context_is_passed_through_to_the_template(self):
        """Regression guard: a mis-wired context would silently render every variable empty."""
        obj = SimpleNamespace(name="AMS-195")
        self.assertEqual(render_jinja2_for_regex("{{ object.name }}", {"object": obj}), r"AMS\-195")

    def test_rendering_is_still_sandboxed(self):
        with self.assertRaises(SecurityError):
            render_jinja2_for_regex("{{ ''.__class__.__name__ }}", {})
