from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Dict, List, Tuple


def _parse_amount(value: str) -> Decimal:
    """Parse amount safely and normalize to 2 decimals."""
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError) as exc:
        raise ValueError(f"Invalid amount: {value}") from exc
    return amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def _normalize_country(country: str) -> str:
    if not country:
        return "UNKNOWN"
    return country.strip().upper()


def _normalize_timestamp(raw_ts: str) -> str:
    """
    Normalize timestamp to ISO UTC.
    Expected format example: 2026-05-08T10:30:00Z
    """
    if not raw_ts:
        raise ValueError("event_time is required")
    dt = datetime.strptime(raw_ts, "%Y-%m-%dT%H:%M:%SZ")
    return dt.replace(tzinfo=timezone.utc).isoformat()


def transform_record(record: Dict) -> Dict:
    """
    Convert raw input record into analytics-ready record.
    """
    customer_id = str(record.get("customer_id", "")).strip()
    if not customer_id:
        raise ValueError("customer_id is required")

    transformed = {
        "batch_id": str(record.get("batch_id", "")).strip() or "NA",
        "customer_id": customer_id,
        "country": _normalize_country(record.get("country", "")),
        "amount": str(_parse_amount(record.get("amount", "0"))),
        "currency": str(record.get("currency", "USD")).strip().upper(),
        "event_time_utc": _normalize_timestamp(record.get("event_time", "")),
        "is_high_value": _parse_amount(record.get("amount", "0")) >= Decimal("1000.00"),
    }
    return transformed


def transform_batch(records: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
    """
    Returns:
      - valid_records: transformed records
      - rejected_records: original records with error message
    """
    valid_records: List[Dict] = []
    rejected_records: List[Dict] = []

    for record in records:
        try:
            valid_records.append(transform_record(record))
        except Exception as exc:  # noqa: BLE001
            rejected = dict(record)
            rejected["error"] = str(exc)
            rejected_records.append(rejected)

    return valid_records, rejected_records

