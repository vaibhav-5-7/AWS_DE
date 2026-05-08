import json
import tempfile
import unittest
from pathlib import Path

from src.batch_processor.handler import lambda_handler, run_batch


class TestHandler(unittest.TestCase):
    def test_lambda_handler_returns_counts(self):
        event = {
            "records": [
                {
                    "batch_id": "B1",
                    "customer_id": "C1",
                    "country": "in",
                    "amount": "10",
                    "currency": "inr",
                    "event_time": "2026-01-01T00:00:00Z",
                },
                {
                    "batch_id": "B1",
                    "customer_id": "",
                    "country": "in",
                    "amount": "10",
                    "currency": "inr",
                    "event_time": "2026-01-01T00:00:00Z",
                },
            ]
        }

        response = lambda_handler(event, None)
        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(response["body"]["success_count"], 1)
        self.assertEqual(response["body"]["rejected_count"], 1)

    def test_run_batch_writes_output_file(self):
        sample_input = [
            {
                "batch_id": "B1",
                "customer_id": "C1",
                "country": "in",
                "amount": "10",
                "currency": "inr",
                "event_time": "2026-01-01T00:00:00Z",
            }
        ]

        with tempfile.TemporaryDirectory() as tmp:
            input_path = Path(tmp) / "input.json"
            output_path = Path(tmp) / "output.json"
            input_path.write_text(json.dumps(sample_input), encoding="utf-8")

            output = run_batch(str(input_path), str(output_path))
            output_file = json.loads(output_path.read_text(encoding="utf-8"))

            self.assertEqual(output["summary"]["success_count"], 1)
            self.assertEqual(output, output_file)


if __name__ == "__main__":
    unittest.main()

