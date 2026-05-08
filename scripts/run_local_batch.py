import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.batch_processor.handler import run_batch


if __name__ == "__main__":
    result = run_batch(
        input_path="tests/data/input_batch.json",
        output_path="output/batch_output.json",
    )
    print("Batch completed:", result["summary"])

