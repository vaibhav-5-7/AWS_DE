# AWS Batch Starter (Pure Python)

This starter project shows how to build a simple batch transformation pipeline that can be used in:
- AWS Lambda (small-medium batches),
- AWS Glue Python Shell jobs (pure Python),
- Redshift loading flows (via SQL + COPY patterns).

No external libraries are used. No pandas/numpy/pyspark.

## 1) Project structure

```text
AWS_DE/
  src/
    batch_processor/
      __init__.py
      transform.py
      handler.py
      redshift_sql.py
  tests/
    data/
      input_batch.json
      expected_valid_batch.json
    test_transform.py
    test_handler.py
  scripts/
    run_local_batch.py
  requirements.txt
  README.md
```

## 2) What this code does

1. Reads raw batch records (JSON list).
2. Applies transformations and validation:
   - country uppercase,
   - amount normalized to 2 decimals,
   - timestamp normalized to UTC ISO format,
   - high-value flag for amount >= 1000.
3. Splits output into:
   - `valid_records`
   - `rejected_records` with `error` reason.
4. Provides SQL helpers for Redshift COPY + upsert pattern.

## 3) Run in VS Code terminal

Use Python 3.11+ if possible.

```bash
python3 -m unittest discover -s tests -v
python3 scripts/run_local_batch.py
```

Generated output file:
- `output/batch_output.json`

## 4) Unit testing approach (pure)

- `unittest` from standard library.
- test data kept under `tests/data/`.
- tests cover:
  - valid transformation,
  - validation failure,
  - batch split (success vs rejected),
  - local runner and lambda handler.

## 5) How to connect with AWS services

### Lambda
- Use `lambda_handler` from `src/batch_processor/handler.py`.
- Input event must have:
  - `records` (list of dicts).

### Glue Python Shell Job
- Create Glue job (Python Shell, not Spark).
- Package source code as zip and run a small entry script similar to `scripts/run_local_batch.py`.
- Read input from S3 and write transformed JSON back to S3.

### Redshift
Typical flow:
1. Write transformed batch JSON to S3.
2. Use Redshift `COPY` into staging table.
3. Run generated upsert SQL from `redshift_sql.py`.

## 6) Git + GitHub workflow (beginner friendly)

Run from project root:

```bash
git init
git add .
git commit -m "Initial pure Python batch pipeline with unit tests"
git branch -M main
git remote add origin <YOUR_GITHUB_REPO_URL>
git push -u origin main
```

## 7) Branching and production merge flow

For each new change:

```bash
git checkout -b feature/batch-change-1
# do code changes
python3 -m unittest discover -s tests -v
git add .
git commit -m "Add batch change 1"
git push -u origin feature/batch-change-1
```

Then open Pull Request in GitHub:
- base: `main`
- compare: `feature/batch-change-1`

Before merge:
- all checks/tests pass
- 1 reviewer approval

Merge strategy:
- Use **Squash and merge** for clean history.

After merge:

```bash
git checkout main
git pull origin main
git branch -d feature/batch-change-1
```

## 8) Production checklist

- unit tests passed
- test data includes edge cases
- no secrets in code
- environment-specific values from env variables
- rollback plan ready

---

If you want next step, we can add:
1. S3 read/write utility (pure Python + boto3),
2. Real Lambda deployment zip command,
3. GitHub Actions pipeline for unit tests on each PR.

# AWS_DE
