from typing import List


def build_redshift_upsert_sql(schema: str, table: str, staging_table: str) -> str:
    """
    Creates SQL used after loading transformed data to staging table.
    """
    return f"""
BEGIN;

DELETE FROM {schema}.{table}
USING {schema}.{staging_table}
WHERE {table}.batch_id = {staging_table}.batch_id
  AND {table}.customer_id = {staging_table}.customer_id;

INSERT INTO {schema}.{table}
(
  batch_id,
  customer_id,
  country,
  amount,
  currency,
  event_time_utc,
  is_high_value
)
SELECT
  batch_id,
  customer_id,
  country,
  amount,
  currency,
  event_time_utc,
  is_high_value
FROM {schema}.{staging_table};

COMMIT;
""".strip()


def build_copy_command(
    schema: str,
    staging_table: str,
    s3_path: str,
    iam_role_arn: str,
    region: str = "ap-south-1",
) -> str:
    return (
        f"COPY {schema}.{staging_table} "
        f"FROM '{s3_path}' "
        f"IAM_ROLE '{iam_role_arn}' "
        "FORMAT AS JSON 'auto' "
        f"REGION '{region}' "
        "TIMEFORMAT 'auto' "
        "TRUNCATECOLUMNS BLANKSASNULL EMPTYASNULL;"
    )


def required_columns() -> List[str]:
    return [
        "batch_id",
        "customer_id",
        "country",
        "amount",
        "currency",
        "event_time_utc",
        "is_high_value",
    ]

