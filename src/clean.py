"""Tasks 2 and 3: Explore and clean the raw DataFrames."""
import logging
from pathlib import Path

import pandas as pd


def load_and_explore(data_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Task 2: Load both CSV files and explore their contents before cleaning."""
    # TODO: Read messy_sales.csv and messy_customers.csv with pd.read_csv().
    # TODO: For each DataFrame call .info(), .describe(), .head(20), and .isna().sum().
    # TODO: Log what you discover (e.g. which columns have nulls, any suspicious values).
    raise NotImplementedError("Task 2: implement load_and_explore")


def clean_sales(sales: pd.DataFrame) -> pd.DataFrame:
    """Task 3: Clean the sales DataFrame using vectorized Pandas operations."""
    # TODO: Normalize product_name with .str.strip().str.title().
    # TODO: Normalize customer_email with .str.lower().str.strip().
    # TODO: Convert price to numeric with pd.to_numeric(errors="coerce").
    # TODO: Parse date with pd.to_datetime(errors="coerce").
    # TODO: Drop rows where product_name is missing.
    # TODO: Drop rows where price is negative.
    # TODO: Drop rows where quantity is zero.
    # TODO: Drop rows where date is NaT (invalid after parsing).
    # TODO: Remove duplicate transactions: .drop_duplicates(subset="transaction_id", keep="first").
    # TODO: Decide what to do with outlier prices (clip, flag, or leave) and add a comment explaining why.
    raise NotImplementedError("Task 3: implement clean_sales")
