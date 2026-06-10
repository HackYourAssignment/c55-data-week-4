# AI Assist Report

## The prompt I gave

I asked an LLM to help implement a Week 4 Pandas pipeline for the MessyCorp assignment. The tasks were to download CSV inputs from Azure Blob Storage, explore the raw data, clean sales data with vectorized Pandas operations, join customer data, build report tables with groupby named aggregations, and write CSV/Parquet/chart outputs.

## The code it suggested

The LLM suggested using:

- `DefaultAzureCredential` and `BlobServiceClient` for downloading input files from Azure.
- `pd.read_csv()` for loading `messy_sales.csv` and `messy_customers.csv`.
- `.str.strip().str.title()` to normalize product names.
- `.str.lower().str.strip()` to normalize customer emails.
- `pd.to_numeric(..., errors="coerce")` for price conversion.
- `pd.to_datetime(..., errors="coerce")` for date parsing.
- Boolean filters for removing bad rows.
- `.drop_duplicates(subset="transaction_id", keep="first")` for duplicate transactions.
- `merge(..., how="inner")` for joining sales and customers.
- A vectorized `is_high_value` column based on `price * quantity >= 150`.
- `groupby().agg(...)` with named aggregations for report tables.
- `to_csv()`, `to_parquet()`, and `plt.savefig()` for outputs.

## What I changed and why

I followed the assignment comments closely and implemented the code step by step. I left out Task 7 upload functionality for now because it is extra credit. I kept the outlier price values unchanged and added a comment explaining that decision, because the assignment does not define a business rule for clipping or removing outlier prices.

I also used `matplotlib.use("Agg")` before importing `pyplot` so the chart can be generated in headless environments.

## Did it work?

Yes. Tasks 1–6 worked successfully. The pipeline downloads the input CSV files from Azure, explores the raw data, cleans the sales data, joins it with customer data, builds the report tables, and writes the CSV, Parquet, and PNG chart outputs.

The main thing I learned was how Pandas replaces manual row-by-row loops with vectorized operations, boolean filters, joins, and groupby aggregations.
