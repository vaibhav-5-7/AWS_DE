import json
import unittest
from pathlib import Path

from src.batch_processor.transform import transform_batch, transform_record


def _read_json(path: str):
    return json.loads(Path(path).read_text(encoding="utf-8"))


class TestTransformRecord(unittest.TestCase):
    def test_transform_single_valid_record(self):
        raw = {
            "batch_id": "BATCH_001",
            "customer_id": "CUST_100",
            "country": "in",
            "amount": "1000",
            "currency": "inr",
            "event_time": "2026-05-08T12:00:00Z",
        }

        transformed = transform_record(raw)

        self.assertEqual(transformed["country"], "IN")
        self.assertEqual(transformed["amount"], "1000.00")
        self.assertTrue(transformed["is_high_value"])
        self.assertEqual(transformed["event_time_utc"], "2026-05-08T12:00:00+00:00")

    def test_transform_fails_if_customer_missing(self):
        raw = {
            "batch_id": "BATCH_001",
            "customer_id": "",
            "country": "in",
            "amount": "100",
            "currency": "inr",
            "event_time": "2026-05-08T12:00:00Z",
        }

        with self.assertRaises(ValueError):
            transform_record(raw)


class TestTransformBatch(unittest.TestCase):
    def test_batch_splits_valid_and_rejected_records(self):
        input_data = _read_json("tests/data/input_batch.json")
        expected_valid = _read_json("tests/data/expected_valid_batch.json")

        valid, rejected = transform_batch(input_data)

        self.assertEqual(valid, expected_valid)
        self.assertEqual(len(rejected), 2)
        self.assertIn("error", rejected[0])
        self.assertIn("error", rejected[1])


if __name__ == "__main__":
    unittest.main()

