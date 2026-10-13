"""Helpers for safely evaluating user-authored regular expressions.

Data validation rules match operator-supplied patterns against arbitrary user-supplied data on the
request path. Python's standard `re` module offers no way to bound backtracking, so a pattern that
backtracks catastrophically consumes worker time without limit when evaluated against a
non-matching subject (ReDoS, CWE-1333). The third-party `regex` module supports a per-call
`timeout`, so every "stored pattern versus request data" match is routed through this module.

These mirror helpers that newer Nautobot releases provide in `nautobot.apps.utils`; they are
duplicated here so that this app does not depend on a minimum Nautobot patch release.
"""

import logging
import re

import regex
from django.conf import settings
from django.core.exceptions import ValidationError
from django.template import engines

logger = logging.getLogger(__name__)

# Max seconds allowed per untrusted regex match (prevents ReDoS), used when Nautobot does not
# provide a `REGEX_TIMEOUT` setting.
REGEX_TIMEOUT_DEFAULT = 1.0


class InvalidRegexError(ValidationError):
    """A stored regular expression could not be compiled, so the value under test is rejected."""


class RegexTimeoutError(ValidationError):
    """Matching exceeded the allowed time, so the value under test is rejected."""


def compile_regex(pattern):
    """Compile `pattern` with the `regex` module, which supports bounded matching.

    Args:
        pattern (str): The regular expression to compile.

    Returns:
        (regex.Pattern): The compiled pattern.

    Raises:
        InvalidRegexError: If `pattern` is not a valid regular expression.
    """
    try:
        return regex.compile(pattern)
    except (regex.error, TypeError, ValueError, RecursionError) as exc:
        raise InvalidRegexError(f"{pattern!r} is not a valid regular expression: {exc}", code="regex_invalid") from exc


def regex_match(pattern, value, *, timeout=None):
    """As `re.match()`, but abort the attempt after `timeout` seconds.

    Args:
        pattern (str): The regular expression to match with.
        value (str): The value to match against.
        timeout (float): Seconds to allow; defaults to Nautobot's `REGEX_TIMEOUT` setting if defined,
            otherwise `REGEX_TIMEOUT_DEFAULT`.

    Returns:
        (regex.Match): The match, or `None` if `value` does not match.

    Raises:
        InvalidRegexError: If `pattern` is not a valid regular expression.
        RegexTimeoutError: If matching did not complete within `timeout`.

    Both exceptions are `ValidationError` subclasses, so a caller that does not catch them fails
    closed: the value under test is rejected rather than silently accepted.
    """
    compiled = compile_regex(pattern)
    # Read here rather than bound as a default argument so that `override_settings` takes effect.
    # `REGEX_TIMEOUT` only exists in newer Nautobot releases, hence the fallback.
    if timeout is None:
        timeout = getattr(settings, "REGEX_TIMEOUT", REGEX_TIMEOUT_DEFAULT)
    try:
        return compiled.match(value, timeout=timeout)
    except TimeoutError as exc:
        # Logged as well as raised: the validation error reaches the user who submitted the value,
        # but it is the operator who has to find and fix the stored pattern.
        logger.error("Regular expression %r exceeded the %s second matching timeout and was aborted.", pattern, timeout)
        raise RegexTimeoutError(
            f"Matching against the regular expression {pattern!r} exceeded {timeout} second(s) and was aborted; "
            "the pattern may be subject to catastrophic backtracking. Please simplify the expression.",
            code="regex_timeout",
        ) from exc


def _escape_regex_metacharacters(value):
    """Jinja2 `finalize` hook that renders an interpolated value as a regex literal."""
    # Jinja passes the raw value, which may be an int, None or Undefined, so coerce before escaping.
    return re.escape(str(value))


def _get_regex_jinja2_environment():
    """Jinja2 environment used to render a user-authored template into a regular expression.

    An overlay of the standard environment, so the sandbox, filters and globals are all preserved,
    differing in three ways:

    - `finalize` passes every `{{ ... }}` interpolation through `re.escape()`, so an interpolated
      value can only ever contribute literal characters to the pattern. Literal template text is not
      finalized, so the template author's own regex syntax survives untouched.
    - `autoescape` is off, because HTML escaping is meaningless in a regular expression and would
      otherwise interpolate a value containing `&` as `&amp;`.
    - `loader` is unset, as including a Nautobot HTML template cannot produce a useful pattern.
    """
    parent = engines["jinja"].env
    # Cached on the parent environment so that reconfiguring the template engine, as
    # `override_settings` does in tests, yields a fresh overlay rather than a stale one.
    overlay = getattr(parent, "_nautobot_dve_regex_overlay", None)
    if overlay is None:
        overlay = parent.overlay(autoescape=False, finalize=_escape_regex_metacharacters, loader=None)
        parent._nautobot_dve_regex_overlay = overlay  # pylint: disable=protected-access
    return overlay


def render_jinja2_for_regex(template_code, context):
    """
    Render a Jinja2 template whose result is to be used as a regular expression. Return the rendered content.

    Values interpolated from `context` are regex-escaped and treated as literal text, so that data
    being validated cannot alter the structure of the resulting pattern. There is no opt-out.
    """
    # The raw jinja2 Template is used here rather than django_jinja's wrapper, so the context must be
    # passed positionally; `render(context=context)` would bind a variable literally named "context".
    return _get_regex_jinja2_environment().from_string(template_code).render(context)
