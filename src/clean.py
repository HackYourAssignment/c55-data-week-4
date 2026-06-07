"""Tasks 2 and 3: Explore and clean the raw DataFrames."""
import logging
from pathlib import Path

import pandas as pd


def load_and_explore(data_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Task 2: Load both CSV files and explore their contents before cleaning."""
    data_sales = pd.read_csv(data_dir / "messy_sales.csv")
    data_customers = pd.read_csv(data_dir / "messy_customers.csv")

    logging.info("--- Exploring Data ---")
    logging.info("\n== Sales Data ==")
    data_sales.info()
    logging.info(f"\nDescribe:\n{data_sales.describe()}")
    logging.info(f"\nRows:\n{data_sales.head(20)}")
    logging.info(f"\nMissing Values:\n{data_sales.isna().sum()}")
    logging.info("Exploration of Sales Data is complete.")
    logging.info("\n== Customers Data ==")
    data_customers.info()  
    logging.info(f"\nDescribe:\n{data_customers.describe()}")
    logging.info(f"\nFirst Rows:\n{data_customers.head(20)}")
    logging.info(f"\nMissing Values:\n{data_customers.isna().sum()}")
    logging.info("Exploration of Customers Data is complete.")
    return data_sales, data_customers


def clean_sales(sales: pd.DataFrame) -> pd.DataFrame:
    """Task 3: Clean the sales DataFrame using vectorized Pandas operations."""
    product_name = sales["product_name"].str.strip().str.title()
    sales["product_name"] = product_name
    customer_email = sales["customer_email"].str.lower().str.strip()
    sales["customer_email"] = customer_email
    price = pd.to_numeric(sales["price"], errors="coerce")
    sales["price"] = price
    date = pd.to_datetime(sales["date"], errors="coerce")
    sales["date"] = date
    sales = sales.dropna(subset=["product_name"])
    sales = sales[sales["price"] >= 0]
    sales = sales[sales["quantity"] > 0]
    sales = sales.dropna(subset=["date"])
    sales = sales.drop_duplicates(subset="transaction_id", keep="first")
    logging.info(f"cleaning complete. Rows remaining: {len(sales)}")
    # Decision: Leave outlier prices as they are. Why? Because I think they could be valid values and I need to understand the detalis of the data.
    return sales
