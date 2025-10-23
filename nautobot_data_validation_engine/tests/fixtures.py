"""Create fixtures for tests."""

from nautobot_data_validation_engine.models import RegularExpressionValidationRule


def create_regularexpressionvalidationrule():
    """Fixture to create necessary number of RegularExpressionValidationRule for tests."""
    RegularExpressionValidationRule.objects.create(name="Test One")
    RegularExpressionValidationRule.objects.create(name="Test Two")
    RegularExpressionValidationRule.objects.create(name="Test Three")
