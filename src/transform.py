"""Task 4: Join customer data and add derived columns."""
import logging

import pandas as pd


def join_customers(sales: pd.DataFrame, customers: pd.DataFrame) -> pd.DataFrame:
    """Task 4: Normalize join keys, merge, and add a derived boolean flag."""
    customers["customer_email"] = customers["customer_email"].str.lower().str.strip()
    sales["customer_email"] = sales["customer_email"].str.lower().str.strip()
    merged = sales.merge(customers, on="customer_email", how="inner")
    merged["revenue"] = merged["price"] * merged["quantity"]
    merged["is_high_value"] = merged["revenue"] >= 150
    # TODO: (Optional hands-on) Try a left join instead and inspect rows where customer_name is NaN.
    logging.info("Joining complete. Rows in merged DataFrame: %d", len(merged))
    return merged
