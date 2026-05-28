"""Task 4: Join customer data and add derived columns."""
import logging

import pandas as pd


def join_customers(sales: pd.DataFrame, customers: pd.DataFrame) -> pd.DataFrame:
    """Task 4: Normalize join keys, merge, and add a derived boolean flag."""
    sales_clean = sales.copy()
    customers_clean = customers.copy()

    sales_clean["customer_email"] = sales_clean["customer_email"].str.lower().str.strip()
    customers_clean["customer_email"] = customers_clean["customer_email"].str.lower().str.strip()

    sales_merged = pd.merge(sales_clean, customers_clean, on="customer_email", how="inner")

    sales_merged["is_high_value"] = sales_merged["price"] * sales_merged["quantity"] >= 150

    left_join_check = sales_clean.merge(
        customers_clean,
        on="customer_email",
        how="left",
        indicator=True,
    )

    logging.info("Left join value counts:\n%s", left_join_check["_merge"].value_counts())
    logging.info("Joined sales with customers: %s rows remain.", len(sales_merged))


    return sales_merged
