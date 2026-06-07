# AI Assist Report

## The prompt I gave

<!-- Paste the exact prompt you gave the LLM here. -->
I needed help implementing the final part of Task 7 in my Pandas + Azure data pipeline assignment.
## The code it suggested
local_file = output_dir / "customer_summary.parquet"

blob = container.get_blob_client("customer_summary.parquet")
downloaded = blob.download_blob().readall()

remote_df = pd.read_parquet(io.BytesIO(downloaded))
local_df = pd.read_parquet(local_file)

assert len(remote_df) == len(local_df), "Row count mismatch!"

logging.info("Round-trip verification passed ✔")
logging.info(f"Uploaded {len(parquet_files)} files to {container_name}")
```python
# Paste the relevant code the LLM suggested here.
```

## What I changed and why

<!-- Describe what you kept, what you modified, and what you threw away. -->
I did not change the main logic because the round-trip verification approach was already correct.
I kept the assert statement because it is a simple and effective way to validate data consistency.
I kept logging as it helps track successful execution in the pipeline.

## Did it work?

<!-- Yes / partially / no — and what you learned from the interaction. -->
The code worked successfully and uploaded files to Azure and downloaded customer_summary.parquet back from Blob Storage , also verified that the row counts matched without any errors

I learned that the key part of this step is not just uploading files, but ensuring data integrity between local and cloud storage.
