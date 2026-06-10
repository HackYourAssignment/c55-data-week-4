"""Task 4: Join customer data and add derived columns."""
import logging

import pandas as pd


def join_customers(sales: pd.DataFrame, customers: pd.DataFrame) -> pd.DataFrame:
    """Task 4: Normalize join keys, merge, and add a derived boolean flag."""
    sales = sales.copy()
    customers = customers.copy()

    sales["customer_email"] = sales["customer_email"].str.lower().str.strip()
    customers["customer_email"] = customers["customer_email"].str.lower().str.strip()

    orphan_check = sales.merge(customers, on="customer_email", how="left")
    orphan_orders = orphan_check[orphan_check["customer_name"].isna()]

    logging.info("Orphan orders after left join: %s", len(orphan_orders))

    enriched = sales.merge(customers, on="customer_email", how="inner")

    enriched["is_high_value"] = enriched["price"] * enriched["quantity"] >= 150

    logging.info("Rows after inner join: %s", len(enriched))

    return enriched
