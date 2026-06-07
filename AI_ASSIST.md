# AI Assist Report

## The prompt I gave

I asked an LLM for help understanding several Pandas concepts used in the Week 4 assignment, including:

- how to normalize strings with .str.strip() and .str.lower()
- how to use groupby() with named aggregations
- how to merge DataFrames with pd.merge
- how to save plots with Matplotlib in a headless environment
- how to debug Pandas errors such as KeyError after groupby

## The code it suggested

The LLM suggested small examples of:

- vectorized string cleaning
- groupby(...).agg(...)
- pd.merge(..., how="inner")
- .plot(...); plt.savefig(...)
- using as_index=False after groupby

```python
sales["customer_email"] = (
     sales["customer_email"] 
     .str.lower()
     .str.strip()
) 
category_performance = (
     data.groupby("category", as_index=False)
     .agg(
         total_revenue=("revenue", "sum"), order_count=("transaction_id", "nunique"),
    )
)
```

## What I changed and why

I rewrote the examples to fit the assignment and split the logic across clean.py, transform.py, report.py, and ingest.py.

I adjusted the report logic to use the exact column names required by the assignment and fixed several issues manually, including:

- grouped columns becoming indexes after groupby
- plotting errors caused by missing columns
- correct use of index=False
- logging instead of print statements
- proper handling of duplicate rows and missing values

I also tested the pipeline locally before enabling the Azure upload step.

## Did it work?

Yes, partially. The AI explanations were useful for understanding Pandas syntax and debugging errors. The most useful part was understanding how groupby, joins, and vectorized operations work in Pandas.
