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
    # TODO: Create a BlobServiceClient using DefaultAzureCredential and ACCOUNT_URL.
    credential = DefaultAzureCredential()
    blob_service_client = BlobServiceClient(account_url=ACCOUNT_URL, credential=credential) 
    # TODO: Get a container client for SOURCE_CONTAINER.
    container_client = blob_service_client.get_container_client(SOURCE_CONTAINER)
    # TODO: For each filename in FILES, download the blob and write it to data_dir/<filename>.
    for filename in FILES:
       Path("data").mkdir(exist_ok=True)
    for name in FILES:
       blob = container_client.get_blob_client(name)
    with open(f"data/{name}", "wb") as f:
        f.write(blob.download_blob().readall())

    # TODO: Log a message for each downloaded file.
    for filename in FILES:
     logging.info("Downloaded %s", name)


def upload_outputs(output_dir: Path, github_username: str) -> None:
    """Task 7 (extra credit): Upload Parquet outputs to Azure and verify the round-trip."""
    container_name = f"week4-{github_username}"

    # EXTRA CREDIT — implement this after Tasks 2–6 are working.
    # TODO: Create a BlobServiceClient using DefaultAzureCredential and ACCOUNT_URL.
    # TODO: Get (or create) the container named container_name.
    # TODO: Upload every .parquet file in output_dir to the container.
    # TODO: Download customer_summary.parquet back and assert its row count matches the local file.
    # TODO: Log the container name and number of files uploaded.
    
