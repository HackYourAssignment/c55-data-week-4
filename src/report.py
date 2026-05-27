"""Tasks 5 and 6: Build report tables and write outputs."""
import logging
from pathlib import Path

import pandas as pd


def build_reports(enriched: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Task 5: Build four summary tables using groupby and named aggregations."""
    # TODO: Add a week column using .dt.isocalendar().week.
    # TODO: Build weekly_revenue: group by week and region, columns week/region/total_revenue/order_count.
    # TODO: Build customer_summary: group by customer_email, columns customer_email/customer_name/
    #       region/loyalty_tier/total_spent/avg_order/order_count.
    #       Use ("customer_name", "first") to pick the constant-per-group string columns.
    # TODO: Build category_performance: group by category, columns category/total_revenue/order_count.
    # TODO: Build loyalty_analysis: group by loyalty_tier, columns loyalty_tier/avg_spent/customer_count.
    raise NotImplementedError("Task 5: implement build_reports")


def write_outputs(reports: dict[str, pd.DataFrame], output_dir: Path) -> None:
    """Task 6: Write report tables to CSV/Parquet and save a bar chart."""
    output_dir.mkdir(exist_ok=True)

    # TODO: Write reports["weekly_revenue"] to weekly_revenue.csv with index=False.
    # TODO: Write reports["customer_summary"] to customer_summary.parquet with index=False.
    # TODO: Write reports["category_performance"] to category_performance.csv with index=False.
    # TODO: Sort category_performance by total_revenue descending.
    # TODO: Plot a bar chart (x="category", y="total_revenue") and save to category_revenue.png
    #       using plt.savefig(output_dir / "category_revenue.png", bbox_inches="tight").
    #       Use matplotlib.use("Agg") before importing pyplot for headless environments.
    raise NotImplementedError("Task 6: implement write_outputs")
