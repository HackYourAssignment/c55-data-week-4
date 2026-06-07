"""MessyCorp Pandas pipeline — Task 1 through 7 runner."""
import logging
from pathlib import Path

from src.ingest import download_inputs, upload_outputs
from src.clean import load_and_explore, clean_sales
from src.transform import join_customers
from src.report import build_reports, write_outputs

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

DATA_DIR = Path("data")
OUTPUT_DIR = Path("output")

# TODO (Task 7): replace with your GitHub username before running the pipeline.
GITHUB_USERNAME = "hannahwn"


def run() -> None:
    download_inputs(DATA_DIR)

    sales_raw, customers_raw = load_and_explore(DATA_DIR)

    sales_clean = clean_sales(sales_raw)
    enriched = join_customers(sales_clean, customers_raw)

    reports = build_reports(enriched)
    write_outputs(reports, OUTPUT_DIR)

    upload_outputs(OUTPUT_DIR, GITHUB_USERNAME)

    logging.info("Pipeline complete.")


if __name__ == "__main__":
    run()
