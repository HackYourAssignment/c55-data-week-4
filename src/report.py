"""Tasks 5 and 6: Build report tables and write outputs."""
import logging
from pathlib import Path

import pandas as pd


def build_reports(enriched: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Task 5: Build four summary tables using groupby and named aggregations."""
    # TODO: Add a week column using .dt.isocalendar().week.
    enriched["week"] = enriched["date"].dt.isocalendar().week
    # TODO: Build weekly_revenue: group by week and region, columns week/region/total_revenue/order_count.
    enriched["revenue"] = enriched["price"] * enriched["quantity"]
    weekly_revenue = enriched.groupby(["week", "region"]).agg(
        total_revenue=pd.NamedAgg(column="revenue", aggfunc="sum"),
        order_count=pd.NamedAgg(column="transaction_id", aggfunc="count"),
    ).reset_index()
    # TODO: Build customer_summary: group by customer_email, columns customer_email/customer_name/
    #       region/loyalty_tier/total_spent/avg_order/order_count.
    #       Use ("customer_name", "first") to pick the constant-per-group string columns.
    customer_summary = enriched.groupby("customer_email").agg(
        customer_name=pd.NamedAgg(column="customer_name", aggfunc="first"),
        region=pd.NamedAgg(column="region", aggfunc="first"),
        loyalty_tier=pd.NamedAgg(column="loyalty_tier", aggfunc="first"),
        total_spent=pd.NamedAgg(column="revenue", aggfunc="sum"),
        avg_order=pd.NamedAgg(column="revenue", aggfunc="mean"),
        order_count=pd.NamedAgg(column="transaction_id", aggfunc="count"),
    ).reset_index()
    # TODO: Build category_performance: group by category, columns category/total_revenue/order_count.
    category_performance = enriched.groupby("category").agg(
        total_revenue=pd.NamedAgg(column="revenue", aggfunc="sum"),
        order_count=pd.NamedAgg(column="transaction_id", aggfunc="count"),
    ).reset_index()
    # TODO: Build loyalty_analysis: group by loyalty_tier, columns loyalty_tier/avg_spent/customer_count.
    loyalty_analysis = enriched.groupby("loyalty_tier").agg(
        avg_spent=pd.NamedAgg(column="revenue", aggfunc="mean"),
        customer_count=pd.NamedAgg(column="customer_email", aggfunc="nunique"),
    ).reset_index()
    return {
        "weekly_revenue": weekly_revenue,
        "customer_summary": customer_summary,
        "category_performance": category_performance,
        "loyalty_analysis": loyalty_analysis,
    }
   

   


def write_outputs(reports: dict[str, pd.DataFrame], output_dir: Path) -> None:
    """Task 6: Write report tables to CSV/Parquet and save a bar chart."""
    output_dir.mkdir(exist_ok=True)

    # TODO: Write reports["weekly_revenue"] to weekly_revenue.csv with index=False.
    reports["weekly_revenue"].to_csv(output_dir / "weekly_revenue.csv", index=False)
    # TODO: Write reports["customer_summary"] to customer_summary.parquet with index=False.
    reports["customer_summary"].to_parquet(output_dir / "customer_summary.parquet", index=False)
    # TODO: Write reports["category_performance"] to category_performance.csv with index=False.
    reports["category_performance"].to_csv(output_dir / "category_performance.csv", index=False)
    # TODO: Sort category_performance by total_revenue descending.
    reports["category_performance"] = reports["category_performance"].sort_values("total_revenue", ascending=False)
    # TODO: Plot a bar chart (x="category", y="total_revenue") and save to category_revenue.png
    #       using plt.savefig(output_dir / "category_revenue.png", bbox_inches="tight").
    #       Use matplotlib.use("Agg") before importing pyplot for headless environments.
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt 
    plt.figure(figsize=(10, 6))
    plt.bar(reports["category_performance"]["category"], reports["category_performance"]["total_revenue"])
    plt.xlabel("Category")
    plt.ylabel("Total Revenue")
    plt.title("Total Revenue by Category")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_dir / "category_revenue.png", bbox_inches="tight")
    logging.info(f"Reports written to {output_dir}.")
 