"""Task 1: Download inputs from Azure. Task 7: Upload outputs back to Azure."""
import io
import logging
from pathlib import Path

import pandas as pd
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

ACCOUNT_URL = "https://sthyfstudentsdemo.blob.core.windows.net"
SOURCE_CONTAINER = "week4-inputs"
FILES = ["messy_sales.csv", "messy_customers.csv"]


def download_inputs(data_dir: Path) -> None:
    """Task 1: Download input CSV files from Azure Blob Storage."""
    credential = DefaultAzureCredential()
    service = BlobServiceClient(account_url=ACCOUNT_URL, credential=credential)
    container = service.get_container_client(SOURCE_CONTAINER)
    
    data_dir.mkdir(exist_ok=True)
    
    for filename in FILES:
        blob = container.get_blob_client(filename)
        output_path = data_dir / filename
        with output_path.open("wb") as file:
            file.write(blob.download_blob().readall())
            
        logging.info("Downloaded %s", filename)


def upload_outputs(output_dir: Path, github_username: str) -> None:
    """Task 7 (extra credit): Upload Parquet outputs to Azure and verify the round-trip."""
    container_name = f"week4-{github_username}"

    credential = DefaultAzureCredential()
    service = BlobServiceClient(account_url=ACCOUNT_URL, credential=credential)

    container = service.get_container_client(container_name)
    if not container.exists():
        container.create_container()

    parquet_files = list(output_dir.glob("*.parquet"))
    for file_path in parquet_files:
        blob = container.get_blob_client(file_path.name)
        with file_path.open("rb") as file:
            blob.upload_blob(file, overwrite=True)
        
        logging.info("Uploaded %s", file_path.name)

    local_customer_summary = pd.read_parquet(output_dir / "customer_summary.parquet")
    blob = container.get_blob_client("customer_summary.parquet")
    downloaded_bytes = blob.download_blob().readall()
    downloaded_customer_summary = pd.read_parquet(io.BytesIO(downloaded_bytes))
    
    assert len(downloaded_customer_summary) == len(local_customer_summary)

    logging.info(
        "Uploaded %s parquet file(s) to container %s",
        len(parquet_files),
        container_name,
    )
