"""Tasks 2 and 3: Explore and clean the raw DataFrames."""
import logging
from pathlib import Path

import pandas as pd


def load_and_explore(data_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Task 2: Load both CSV files and explore their contents before cleaning."""
    sales = pd.read_csv(data_dir / "messy_sales.csv")
    customers = pd.read_csv(data_dir / "messy_customers.csv")

    logging.info("Sales DataFrame info:")
    sales.info()

    logging.info("Customers DataFrame info:")
    customers.info()

    logging.info("Sales describe:\n%s", sales.describe())
    logging.info("Customers describe:\n%s", customers.describe())

    logging.info("Sales first 20 rows:\n%s", sales.head(20))
    logging.info("Customers first 20 rows:\n%s", customers.head(20))

    logging.info("Sales missing values:\n%s", sales.isna().sum())
    logging.info("Customers missing values:\n%s", customers.isna().sum())

    logging.info("Exploration complete. Check missing values, dtypes, and numeric outliers above.")

    return sales, customers


def clean_sales(sales: pd.DataFrame) -> pd.DataFrame:
    """Task 3: Clean the sales DataFrame using vectorized Pandas operations."""
    sales["product_name"] = sales["product_name"].str.strip().str.title()
    sales["customer_email"] = sales["customer_email"].str.lower().str.strip()
    sales["price"] = pd.to_numeric(sales["price"], errors="coerce")
    sales["date"] = pd.to_datetime(sales["date"], errors="coerce")
    sales = sales[sales["product_name"].notna()]
    sales = sales[sales["price"] >= 0]
    sales = sales[sales["quantity"] != 0]
    sales = sales[sales["date"].notna()]
    sales = sales.drop_duplicates(subset="transaction_id", keep="first")

    # Outlier prices are left unchanged because the assignment does not define a business rule for capping prices. Keeping them preserves the original transaction value for reporting.
    logging.info("Cleaned sales rows: %s", len(sales))

    return sales
