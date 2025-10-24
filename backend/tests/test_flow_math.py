from decimal import Decimal

from app.utils.analytics import month_range


def test_month_range_inclusive():
    assert month_range("2024-01", "2024-03") == ["2024-01", "2024-02", "2024-03"]
