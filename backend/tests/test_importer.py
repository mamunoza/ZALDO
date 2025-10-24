from datetime import datetime
from decimal import Decimal

from app.utils.ingestion import compute_hash, normalize_amount, parse_date


def test_parse_date_formats():
    assert parse_date("01/02/2024").date() == datetime(2024, 2, 1).date()
    assert parse_date("2024-02-01").date() == datetime(2024, 2, 1).date()
    assert parse_date("01-02-2024").date() == datetime(2024, 2, 1).date()


def test_normalize_amount():
    assert normalize_amount("1.234,50") == Decimal("1234.50")
    assert normalize_amount("-10") == Decimal("-10")
    assert normalize_amount(1000) == Decimal("1000")


def test_compute_hash_changes_with_description():
    hash_a = compute_hash("user@example.com", "acc", datetime(2024, 2, 1), Decimal("100.00"), "Pago Netflix")
    hash_b = compute_hash("user@example.com", "acc", datetime(2024, 2, 1), Decimal("100.00"), "Pago Spotify")
    assert hash_a != hash_b
