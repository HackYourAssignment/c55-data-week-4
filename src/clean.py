"""Tasks 2 and 3: Explore and clean the raw DataFrames."""
import logging
from pathlib import Path

import pandas as pd


def load_and_explore(data_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Task 2: Load both CSV files and explore their contents before cleaning."""
    # TODO: Read messy_sales.csv and messy_customers.csv with pd.read_csv().
    # TODO: For each DataFrame call .info(), .describe(), .head(20), and .isna().sum().
    # TODO: Log what you discover (e.g. which columns have nulls, any suspicious values).
    sales_path = data_dir / "messy_sales.csv"
    customers_path = data_dir / "messy_customers.csv"

    sales = pd.read_csv(sales_path)
    customers = pd.read_csv(customers_path)

    logging.info("=== SALES INFO ===")
    logging.info(sales.info())

    logging.info("=== CUSTOMERS INFO ===")
    logging.info(customers.info())

    logging.info("=== SALES MISSING VALUES ===")
    logging.info(sales.isna().sum())

    logging.info("=== CUSTOMERS MISSING VALUES ===")
    logging.info(customers.isna().sum())

    logging.info("=== SALES SUMMARY ===")
    logging.info(sales.describe())

    logging.info("=== CUSTOMERS SAMPLE ===")
    logging.info(sales.head(20))

    return sales, customers
    raise NotImplementedError("Task 2: implement load_and_explore")


def clean_sales(sales: pd.DataFrame) -> pd.DataFrame:
    """Task 3: Clean the sales DataFrame using vectorized Pandas operations."""
    df = sales.copy()
    # TODO: Normalize product_name with .str.strip().str.title().
    df["product_name"] = df["product_name"].str.strip().str.title()

    # TODO: Normalize customer_email with .str.lower().str.strip().
    df["customer_email"] = df["customer_email"].str.lower().str.strip()
    # TODO: Convert price to numeric with pd.to_numeric(errors="coerce").
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    # TODO: Parse date with pd.to_datetime(errors="coerce").
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    # TODO: Drop rows where product_name is missing.
    df = df[df["product_name"].notna()]
    df = df[df["price"].notna()]
    df = df[df["price"] >= 0]
    df = df[df["quantity"] > 0]
    df = df[df["date"].notna()]

    # TODO: Drop rows where price is negative.
    df = df.drop_duplicates(subset="transaction_id", keep="first")
    # TODO: Drop rows where quantity is zero.
    
    # TODO: Drop rows where date is NaT (invalid after parsing).
    # TODO: Remove duplicate transactions: .drop_duplicates(subset="transaction_id", keep="first").
    # TODO: Decide what to do with outlier prices (clip, flag, or leave) and add a comment explaining why.
    q99 = df["price"].quantile(0.99)
    df["price"] = df["price"].clip(upper=q99)

    logging.info(f"Cleaned sales rows: {len(df)}")

    return df
    
    raise NotImplementedError("Task 3: implement clean_sales")
