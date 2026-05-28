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
     #Create Azure client
    credential = DefaultAzureCredential()
    service = BlobServiceClient(
        account_url=ACCOUNT_URL,
        credential=credential
    )
    # TODO: Get a container client for SOURCE_CONTAINER.
    container_client = service.get_container_client(SOURCE_CONTAINER)
    # TODO: For each filename in FILES, download the blob and write it to data_dir/<filename>.
    # TODO: Log a message for each downloaded file.
    data_dir.mkdir(parents=True, exist_ok=True)
    for filename in FILES:
        blob = container_client.get_blob_client(filename)

        file_path = data_dir / filename

        with open(file_path, "wb") as f:
            f.write(blob.download_blob().readall())

        logging.info(f"Downloaded {filename} -> {file_path}")



def upload_outputs(output_dir: Path, github_username: str) -> None:
    """Task 7 (extra credit): Upload Parquet outputs to Azure and verify the round-trip."""
    logging.info("Starting upload to Azure...")
    container_name = f"week4-{github_username}"

    # EXTRA CREDIT — implement this after Tasks 2–6 are working.
    # TODO: Create a BlobServiceClient using DefaultAzureCredential and ACCOUNT_URL.

    credential = DefaultAzureCredential()
    service = BlobServiceClient(
        account_url=ACCOUNT_URL,
        credential=credential
    )
    # TODO: Get (or create) the container named container_name.
    container_client = service.get_container_client(container_name)
    try:
        container_client.create_container()
    except Exception as e:
        logging.warning(f"Container might already exist: {e}")

    # TODO: Upload every .parquet file in output_dir to the container.
    parquet_files = list(output_dir.glob("*.parquet"))

    for file_path in parquet_files:
        blob = container_client.get_blob_client(file_path.name)

        with open(file_path, "rb") as data:
            blob.upload_blob(data, overwrite=True)

        logging.info(f"Uploaded {file_path.name}")
    # TODO: Download customer_summary.parquet back and assert its row count matches the local file.
    # TODO: Log the container name and number of files uploaded.
    local_file = output_dir / "customer_summary.parquet"

    blob = container_client.get_blob_client("customer_summary.parquet")
    downloaded = blob.download_blob().readall()

    remote_df = pd.read_parquet(io.BytesIO(downloaded))
    local_df = pd.read_parquet(local_file)

    assert len(remote_df) == len(local_df), "Row count mismatch!"

    logging.info("Round-trip verification passed ✔")
    logging.info(f"Uploaded {len(parquet_files)} files to {container_name}")
