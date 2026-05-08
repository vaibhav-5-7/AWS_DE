import json
from pathlib import Path
from typing import Dict, List

from .transform import transform_batch


def _read_json(path: str) -> List[Dict]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _write_json(path: str, payload: Dict) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(payload, indent=2), encoding="utf-8")


def run_batch(input_path: str, output_path: str) -> Dict:
    """
    Local batch runner.
    - Reads raw json list
    - Transforms records
    - Writes valid and rejected records
    """
    records = _read_json(input_path)
    valid, rejected = transform_batch(records)

    payload = {
        "summary": {
            "input_count": len(records),
            "success_count": len(valid),
            "rejected_count": len(rejected),
        },
        "valid_records": valid,
        "rejected_records": rejected,
    }
    _write_json(output_path, payload)
    return payload


def lambda_handler(event, _context):
    """
    Event example:
    {
      "records": [ ... ]
    }
    """
    records = event.get("records", [])
    valid, rejected = transform_batch(records)
    return {
        "statusCode": 200,
        "body": {
            "success_count": len(valid),
            "rejected_count": len(rejected),
            "valid_records": valid,
            "rejected_records": rejected,
        },
    }

