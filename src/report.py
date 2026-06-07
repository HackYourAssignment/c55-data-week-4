"""Tasks 5 and 6: Build report tables and write outputs."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import logging
from pathlib import Path
import pandas as pd


def build_reports(enriched: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Task 5: Build four summary tables using groupby and named aggregations."""
    week = enriched["date"].dt.isocalendar().week
    enriched["week"] = week
    weekly_revenue = enriched.groupby(["week", "region"], as_index=False).agg(
        total_revenue=("revenue", "sum"), order_count=("transaction_id", "count")
    )
    customer_summary = enriched.groupby("customer_email", as_index=False).agg(
        customer_name=("customer_name", "first"),
        region=("region", "first"),
        loyalty_tier=("loyalty_tier", "first"),
        total_spent=("revenue", "sum"),
        avg_order=("revenue", "mean"),
        order_count=("transaction_id", "count"),
    )
    category_performance = enriched.groupby("category", as_index=False).agg(
        total_revenue=("revenue", "sum"), order_count=("transaction_id", "count")
    )
    loyalty_analysis = enriched.groupby("loyalty_tier", as_index=False).agg(
        avg_spent=("revenue", "mean"), customer_count=("customer_email", "nunique")
    )
    return {
        "weekly_revenue": weekly_revenue,
        "customer_summary": customer_summary,
        "category_performance": category_performance,
        "loyalty_analysis": loyalty_analysis,
    }


def write_outputs(reports: dict[str, pd.DataFrame], output_dir: Path) -> None:
    """Task 6: Write report tables to CSV/Parquet and save a bar chart."""
    output_dir.mkdir(exist_ok=True)
    reports["weekly_revenue"].to_csv(output_dir / "weekly_revenue.csv", index=False)
    reports["customer_summary"].to_parquet(
        output_dir / "customer_summary.parquet", index=False
    )
    cat_df = reports["category_performance"].sort_values(
        by="total_revenue", ascending=False
    )
    cat_df.to_csv(output_dir / "category_performance.csv", index=False)
    plt.figure(figsize=(10, 6))
    plt.bar(
        cat_df["category"], cat_df["total_revenue"], color="skyblue", edgecolor="black"
    )
    plt.title("Total Revenue by Category")
    plt.xlabel("Category")
    plt.ylabel("Total Revenue")
    plt.xticks(rotation=45)
    plt.savefig(output_dir / "category_revenue.png", bbox_inches="tight")
    plt.close()
