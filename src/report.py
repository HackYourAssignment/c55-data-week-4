"""Tasks 5 and 6: Build report tables and write outputs."""
import logging
from pathlib import Path

import pandas as pd
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt


def build_reports(enriched: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Task 5: Build four summary tables using groupby and named aggregations."""
    df = enriched.copy()

    # TODO: Add a week column using .dt.isocalendar().week.
    df["week"] = df["date"].dt.isocalendar().week

    # TODO: Build weekly_revenue: group by week and region, columns week/region/total_revenue/order_count.
    weekly_revenue = (
        df.groupby(["week", "region"])
        .agg(
            total_revenue=("price", lambda x: (x * df.loc[x.index, "quantity"]).sum()),
            order_count=("transaction_id", "count")
        )
        .reset_index()
    )

    # TODO: Build customer_summary: group by customer_email, columns customer_email/customer_name/
    #       region/loyalty_tier/total_spent/avg_order/order_count.
    #       Use ("customer_name", "first") to pick the constant-per-group string columns.
    customer_summary = (
        df.groupby("customer_email")
        .agg(
            customer_name=("customer_name", "first"),
            region=("region", "first"),
            loyalty_tier=("loyalty_tier", "first"),
            total_spent=("price", lambda x: (x * df.loc[x.index, "quantity"]).sum()),
            avg_order=("price", lambda x: (x * df.loc[x.index, "quantity"]).mean()),
            order_count=("transaction_id", "count")
        )
        .reset_index()
    )
    # TODO: Build category_performance: group by category, columns category/total_revenue/order_count.
    category_performance = (
        df.groupby("category")
        .agg(
            total_revenue=("price", lambda x: (x * df.loc[x.index, "quantity"]).sum()),
            order_count=("transaction_id", "count")
        )
        .reset_index()
    )
    # TODO: Build loyalty_analysis: group by loyalty_tier, columns loyalty_tier/avg_spent/customer_count.
    loyalty_analysis = (
        df.groupby("loyalty_tier")
        .agg(
            avg_spent=("price", lambda x: (x * df.loc[x.index, "quantity"]).mean()),
            customer_count=("customer_email", "nunique")
        )
        .reset_index()
    )

    logging.info("Reports built successfully")

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

    reports["customer_summary"].to_parquet(
        output_dir / "customer_summary.parquet",
        index=False
    )

    reports["category_performance"].to_csv(
        output_dir / "category_performance.csv",
        index=False
    )
    # TODO: Write reports["customer_summary"] to customer_summary.parquet with index=False.
    cat = reports["category_performance"].sort_values(
        "total_revenue",
        ascending=False
    )

    # TODO: Write reports["category_performance"] to category_performance.csv with index=False.
    plt.figure()
    cat.plot(
        kind="bar",
        x="category",
        y="total_revenue",
        title="Revenue by category"
    )
    # TODO: Sort category_performance by total_revenue descending.
    plt.savefig(output_dir / "category_revenue.png", bbox_inches="tight")

    logging.info(f"Outputs written to {output_dir}")
    # TODO: Plot a bar chart (x="category", y="total_revenue") and save to category_revenue.png
    #       using plt.savefig(output_dir / "category_revenue.png", bbox_inches="tight").
    #       Use matplotlib.use("Agg") before importing pyplot for headless environments.
