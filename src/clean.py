"""Tasks 2 and 3: Explore and clean the raw DataFrames."""
import logging
from pathlib import Path

import pandas as pd


def load_and_explore(data_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Task 2: Load both CSV files and explore their contents before cleaning."""
    # TODO: Read messy_sales.csv and messy_customers.csv with pd.read_csv().
    sales_df = pd.read_csv(data_dir / "messy_sales.csv")
    customers_df = pd.read_csv(data_dir / "messy_customers.csv")
    # TODO: For each DataFrame call .info(), .describe(), .head(20), and .isna().sum().
    logging.info("Sales DataFrame info:\n%s", sales_df.info())
    logging.info("Sales DataFrame description:\n%s", sales_df.describe())
    logging.info("Sales DataFrame head:\n%s", sales_df.head(20))
    logging.info("Sales DataFrame null counts:\n%s", sales_df.isna().sum())
    logging.info("Customers DataFrame info:\n%s", customers_df.info())
    logging.info("Customers DataFrame description:\n%s", customers_df.describe())
    logging.info("Customers DataFrame head:\n%s", customers_df.head(20))
    logging.info("Customers DataFrame null counts:\n%s", customers_df.isna().sum())
    # TODO: Log what you discover (e.g. which columns have nulls, any suspicious values).
    logging.info("Sales DataFrame has %d rows and %d columns", sales_df.shape[0], sales_df.shape[1])
    logging.info("Customers DataFrame has %d rows and %d columns", customers_df.shape[0], customers_df.shape[1])
    return sales_df, customers_df


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
    sales = sales.dropna(subset=["price"])
   
    # TODO: Drop rows where quantity is zero.
    sales = sales.dropna(subset=["quantity"])
    
    # TODO: Drop rows where date is NaT (invalid after parsing).
    sales = sales.dropna(subset=["date"])
    # TODO: Remove duplicate transactions: .drop_duplicates(subset="transaction_id", keep="first").
    sales = sales.drop_duplicates(subset="transaction_id", keep="first")
    # TODO: Decide what to do with outlier prices (clip, flag, or leave) and add a comment explaining why.
    # For simplicity, we'll leave outlier prices as they are, but in a real scenario, we might want to investigate them further or apply business rules to handle them.
    return sales
    