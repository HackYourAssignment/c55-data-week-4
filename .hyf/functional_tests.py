"""Functional tests for the Week 4 autograder.

These tests import the student's code and run synthetic inputs through it to
catch behavioural bugs that static greps cannot detect, for example:

  - using `dropna()` where a boolean filter is required (negative prices,
    zero quantities still slipping through to the cleaned output),
  - an indentation bug in `download_inputs` that only writes the last file,
  - hardcoding the literal "data/" path instead of honouring the
    `data_dir` argument.

Each test is worth 2 points in the autograder; 8 tests × 2 = 16 points
(Level 9 — Behavioural correctness).
"""
import sys
from pathlib import Path
from unittest.mock import MagicMock

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

import pandas as pd
import pytest


# ── Fixtures ────────────────────────────────────────────────────────────────


def _messy_sales_df() -> pd.DataFrame:
    """Synthetic sales rows that mirror the bugs Hannah's PR #3 shipped:
    a negative price, a zero quantity, a null product_name, a duplicate
    transaction_id, and an unparseable date."""
    return pd.DataFrame(
        {
            "transaction_id": [1, 2, 3, 4, 5, 6, 7],
            "product_name": [
                "  Laptop  ",
                "MOUSE",
                None,
                "Desk",
                "Chair",
                "Lamp",
                "Lamp",
            ],
            "category": ["Elec", "Elec", "Elec", "Furn", "Furn", "Furn", "Furn"],
            "price": [999.99, 29.99, 4.99, -149.99, 50.0, 25.0, 25.0],
            "quantity": [1, 5, 10, 1, 0, 3, 3],
            "customer_email": [
                "a@x.com",
                "b@x.com",
                "c@x.com",
                "d@x.com",
                "e@x.com",
                "f@x.com",
                "f@x.com",
            ],
            "date": [
                "2024-03-15",
                "2024-03-15",
                "2024-03-15",
                "2024-03-15",
                "2024-03-15",
                "2024-03-15",
                "not_a_date",
            ],
        }
    )


def _sales_for_join() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "transaction_id": [1, 2, 3],
            "product_name": ["A", "B", "C"],
            "price": [200.0, 50.0, 100.0],
            "quantity": [1, 1, 1],
            "customer_email": [
                "Alice@Example.com  ",
                "  bob@x.com",
                "ghost@nowhere.com",
            ],
        }
    )


def _customers_for_join() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "customer_email": ["alice@example.com", "  BOB@X.COM"],
            "customer_name": ["Alice", "Bob"],
            "region": ["NL", "BE"],
        }
    )


# ── clean_sales ─────────────────────────────────────────────────────────────


def test_clean_sales_removes_negative_prices():
    from src.clean import clean_sales

    cleaned = clean_sales(_messy_sales_df())
    assert (cleaned["price"] >= 0).all(), (
        "clean_sales must drop rows where price is negative — use a boolean "
        "filter (sales[sales['price'] >= 0]), not dropna()."
    )


def test_clean_sales_removes_zero_quantities():
    from src.clean import clean_sales

    cleaned = clean_sales(_messy_sales_df())
    assert (cleaned["quantity"] != 0).all(), (
        "clean_sales must drop rows where quantity is zero — use a boolean "
        "filter (sales[sales['quantity'] != 0]), not dropna()."
    )


def test_clean_sales_drops_nulls_and_bad_dates():
    from src.clean import clean_sales

    cleaned = clean_sales(_messy_sales_df())
    assert cleaned["product_name"].notna().all(), (
        "clean_sales must drop rows where product_name is null."
    )
    assert cleaned["date"].notna().all(), (
        "clean_sales must drop rows where date couldn't be parsed (NaT after "
        "pd.to_datetime with errors='coerce')."
    )


def test_clean_sales_dedupes_and_normalizes_strings():
    from src.clean import clean_sales

    cleaned = clean_sales(_messy_sales_df())
    assert cleaned["transaction_id"].is_unique, (
        "clean_sales must drop duplicate transaction_ids "
        "(drop_duplicates(subset='transaction_id', keep='first'))."
    )
    names = cleaned["product_name"].tolist()
    assert any(n == "Laptop" for n in names), (
        "clean_sales must normalize product_name with .str.strip().str.title() "
        "— '  Laptop  ' should become 'Laptop'."
    )


# ── join_customers ──────────────────────────────────────────────────────────


def test_join_customers_inner_drops_unmatched_sales():
    from src.transform import join_customers

    out = join_customers(_sales_for_join(), _customers_for_join())
    emails = out["customer_email"].astype(str).str.lower().str.strip().tolist()
    assert "ghost@nowhere.com" not in emails, (
        "join_customers must use an inner join — sales rows without a "
        "matching customer should not appear in the output."
    )


def test_join_customers_normalizes_email_for_join():
    from src.transform import join_customers

    out = join_customers(_sales_for_join(), _customers_for_join())
    assert len(out) == 2, (
        "join_customers must normalize customer_email "
        "(.str.lower().str.strip()) on both sides before merging — otherwise "
        "'Alice@Example.com  ' will not match 'alice@example.com'."
    )


def test_join_customers_is_high_value_threshold():
    from src.transform import join_customers

    out = join_customers(_sales_for_join(), _customers_for_join())
    assert "is_high_value" in out.columns, (
        "join_customers must add a vectorized boolean column is_high_value."
    )
    alice = out[out["customer_name"] == "Alice"].iloc[0]
    bob = out[out["customer_name"] == "Bob"].iloc[0]
    assert bool(alice["is_high_value"]) is True, (
        "is_high_value must be True when price * quantity >= 150 "
        "(Alice: 200 * 1 = 200)."
    )
    assert bool(bob["is_high_value"]) is False, (
        "is_high_value must be False when price * quantity < 150 "
        "(Bob: 50 * 1 = 50)."
    )


# ── download_inputs ─────────────────────────────────────────────────────────


def test_download_inputs_writes_all_files_to_data_dir(tmp_path, monkeypatch):
    """The cardinal Hannah-bug to catch: an indentation error that writes
    only the last file, or a hardcoded 'data/' path that ignores the
    data_dir argument. Both make this test fail because files won't appear
    under the tmp_path we pass in."""
    from src import ingest

    fake_contents = {
        "messy_sales.csv": b"transaction_id,price\n1,10.0\n",
        "messy_customers.csv": b"customer_email,customer_name\na@x.com,Alice\n",
    }

    def fake_get_blob_client(name):
        bc = MagicMock()
        bc.download_blob.return_value.readall.return_value = fake_contents[name]
        return bc

    def fake_download_blob(name):
        blob = MagicMock()
        blob.readall.return_value = fake_contents[name]
        return blob

    container_client = MagicMock()
    container_client.get_blob_client.side_effect = fake_get_blob_client
    container_client.download_blob.side_effect = fake_download_blob

    service_client = MagicMock()
    service_client.get_container_client.return_value = container_client

    monkeypatch.setattr(
        ingest, "BlobServiceClient", MagicMock(return_value=service_client)
    )
    monkeypatch.setattr(ingest, "DefaultAzureCredential", MagicMock())

    ingest.download_inputs(tmp_path)

    expected = list(getattr(ingest, "FILES", ["messy_sales.csv", "messy_customers.csv"]))
    missing = [name for name in expected if not (tmp_path / name).exists()]
    assert not missing, (
        f"download_inputs must write every file in FILES to data_dir; "
        f"missing under {tmp_path}: {missing}. Common causes: indentation bug "
        f"(only last file written), or hardcoded 'data/' path instead of "
        f"using the data_dir argument."
    )
