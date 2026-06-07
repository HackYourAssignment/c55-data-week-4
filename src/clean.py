"""Tasks 2 and 3: Explore and clean the raw DataFrames."""
import logging
from pathlib import Path

import pandas as pd


def load_and_explore(data_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Task 2: Load both CSV files and explore their contents before cleaning."""

    sales = pd.read_csv(data_dir / "messy_sales.csv")
    customers = pd.read_csv(data_dir / "messy_customers.csv")

    sales.info()
    sales.describe()
    sales.head(20)
    sales.isna().sum()
    customers.info()
    customers.describe()
    customers.head(20)
    customers.isna().sum()

    logging.info("Sales DataFrame info:")
    logging.info(sales.info())
    logging.info("Customers DataFrame info:")
    logging.info(customers.info())

    return sales, customers


def clean_sales(sales: pd.DataFrame) -> pd.DataFrame:
    """Task 3: Clean the sales DataFrame using vectorized Pandas operations."""
    cleaned = sales.copy()

    cleaned["product_name"] = cleaned["product_name"].str.strip().str.title()

    cleaned["customer_email"] = cleaned["customer_email"].str.lower().str.strip()

    cleaned["price"] = pd.to_numeric(cleaned["price"], errors="coerce")

    cleaned["date"] = pd.to_datetime(cleaned["date"], errors="coerce")

    cleaned = cleaned.dropna(subset=["product_name"])

    cleaned = cleaned[cleaned["price"] >= 0]

    cleaned = cleaned[cleaned["quantity"] != 0]

    cleaned = cleaned.dropna(subset=["date"])

    cleaned = cleaned.drop_duplicates(subset="transaction_id", keep="first")
# Clip prices above 1000 to handle outliers.
    cleaned["price"] = cleaned["price"].clip(upper=1000)

    return cleaned
