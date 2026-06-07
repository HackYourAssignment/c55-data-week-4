"""Tasks 5 and 6: Build report tables and write outputs."""
import logging
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


def build_reports(enriched: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Task 5: Build four summary tables using groupby and named aggregations."""
    data = enriched.copy()

    data["revenue"] = data["price"] * data["quantity"]
    data["week"] = data["date"].dt.isocalendar().week

    weekly_revenue = (
        data.groupby(["week", "region"], as_index=False)
        .agg(
            total_revenue=("revenue", "sum"),
            order_count=("transaction_id", "nunique"),
        )
        .sort_values(["week", "region"])
    )

    customer_summary = (
        data.groupby("customer_email", as_index=False)
        .agg(
            customer_name=("customer_name", "first"),
            region=("region", "first"),
            loyalty_tier=("loyalty_tier", "first"),
            total_spent=("revenue", "sum"),
            avg_order=("revenue", "mean"),
            order_count=("transaction_id", "nunique"),
        )
        .sort_values("total_spent", ascending=False)
    )

    category_performance = (
        data.groupby("category", as_index=False)
        .agg(
            total_revenue=("revenue", "sum"),
            order_count=("transaction_id", "nunique"),
        )
        .sort_values("total_revenue", ascending=False)
    )

    loyalty_analysis = (
        customer_summary.groupby("loyalty_tier", as_index=False)
        .agg(
            avg_spent=("total_spent", "mean"),
            customer_count=("customer_email", "nunique"),
        )
        .sort_values("avg_spent", ascending=False)
    )

    return {
        "weekly_revenue": weekly_revenue,
        "customer_summary": customer_summary,
        "category_performance": category_performance,
        "loyalty_analysis": loyalty_analysis,
    }


def write_outputs(reports: dict[str, pd.DataFrame], output_dir: Path) -> None:
    """Task 6: Write report tables to CSV/Parquet and save a bar chart."""
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    reports["weekly_revenue"].to_csv(
        output_dir / "weekly_revenue.csv",
        index=False,
    )

    reports["customer_summary"].to_parquet(
        output_dir / "customer_summary.parquet",
        index=False,
    )

    reports["category_performance"].to_csv(
        output_dir / "category_performance.csv",
        index=False,
    )

    reports["loyalty_analysis"].to_csv(
        output_dir / "loyalty_analysis.csv",
        index=False,
    )

    category_plot_data = reports["category_performance"].sort_values(
        "total_revenue",
        ascending=False,
    )

    ax = category_plot_data.plot(
        x="category",
        y="total_revenue",
        kind="bar",
        title="Revenue by category",
    )

    ax.set_xlabel("Category")
    ax.set_ylabel("Total revenue")

    plt.tight_layout()
    plt.savefig(output_dir / "category_revenue.png", bbox_inches="tight")
    plt.close()

    logging.info("Written reports to %s", output_dir)
    