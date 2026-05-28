"""Tasks 2 and 3: Explore and clean the raw DataFrames."""

import logging
from pathlib import Path

import pandas as pd


def load_and_explore(data_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Task 2: Load both CSV files and explore their contents before cleaning."""
    # TODO: Read messy_sales.csv and messy_customers.csv with pd.read_csv().
    # TODO: For each DataFrame call .info(), .describe(), .head(20), and .isna().sum().
    # TODO: Log what you discover (e.g. which columns have nulls, any suspicious values).
    messyS = pd.read_csv(data_dir / "messy_sales.csv")
    messyC = pd.read_csv(data_dir / "messy_customers.csv")
    print("--- messy sales info ---")
    messyS.info()
    print()
    print("--- describe ---")
    print(messyS.describe())
    print()
    print("--- head ---")
    print(messyS.head(20))
    print()
    print("--- missing values ---")
    print(messyS.isna().sum())
    print()
    print("--- messy customers info ---")
    messyC.info()
    print()
    print("--- describe ---")
    print(messyC.describe())
    print()
    print("--- head ---")
    print(messyC.head(20))
    print()
    print("--- missing values ---")
    print(messyC.isna().sum())
    return messyS, messyC


def clean_sales(sales: pd.DataFrame) -> pd.DataFrame:
    """Task 3: Clean the sales DataFrame using vectorized Pandas operations."""
    # TODO: Normalize product_name with .str.strip().str.title().
    sales["product_name"] = sales["product_name"].str.strip().str.title()
    # TODO: Normalize customer_email with .str.lower().str.strip().
    sales["customer_email"] = sales["customer_email"].str.lower().str.strip()
    # TODO: Convert price to numeric with pd.to_numeric(errors="coerce").
    sales["price"] = pd.to_numeric(sales["price"], errors="coerce")
    # TODO: Parse date with pd.to_datetime(errors="coerce").
    sales["date"] = pd.to_datetime(sales["date"], errors="coerce")
    # TODO: Drop rows where product_name is missing.
    sales = sales.dropna(subset=["product_name"])
    # TODO: Drop rows where price is negative.
    sales = sales[sales["price"] >= 0]
    # TODO: Drop rows where quantity is zero.
    sales = sales[sales["quantity"] != 0]
    # TODO: Drop rows where date is NaT (invalid after parsing).
    sales = sales.dropna(subset=["date"])
    # TODO: Remove duplicate transactions: .drop_duplicates(subset="transaction_id", keep="first").
    sales = sales.drop_duplicates(subset="transaction_id", keep="first")
    # TODO: Decide what to do with outlier prices (clip, flag, or leave) and add a comment explaining why.
    product_std = sales.groupby("product_name")["price"].transform("std")
    product_mean = sales.groupby("product_name")["price"].transform("mean")
    sales["is_price_outlier"] = sales["price"] > (product_mean + 3 * product_std)
    # since these are sales transactions, we want to keep outliers (they may be real sales of expensive items)
    # but flag them for later just in case for future analysts who may want to filter them out. This way we preserve the data but keep it tracked.
    return sales


load_and_explore(Path("./data"))
