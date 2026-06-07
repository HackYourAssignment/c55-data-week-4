"""Task 4: Join customer data and add derived columns."""
import logging

import pandas as pd


def join_customers(sales: pd.DataFrame, customers: pd.DataFrame) -> pd.DataFrame:
    """Task 4: Normalize join keys, merge, and add a derived boolean flag."""
    # TODO: Normalize customer_email in both DataFrames with .str.lower().str.strip().
    sales["customer_email"] = sales["customer_email"].str.lower().str.strip()
    customers["customer_email"] = customers["customer_email"].str.lower().str.strip()
    # TODO: Merge sales with customers on customer_email using an inner join.
    merged_df = pd.merge(sales, customers, on="customer_email", how="inner")
    # TODO: Add a vectorized boolean column is_high_value: True where price * quantity >= 150.
    merged_df["is_high_value"] = merged_df["price"] * merged_df["quantity"] >= 150
    # TODO: (Optional hands-on) Try a left join instead and inspect rows where customer_name is NaN.
    return merged_df
    
