"""Task 1: Download inputs from Azure. Task 7: Upload outputs back to Azure."""
import io
import logging
from pathlib import Path

import pandas as pd
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError, AzureError

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
        blob_client = container.get_blob_client(filename)
        with open(data_dir / filename, "wb") as f:
            f.write(blob_client.download_blob().readall())
        logging.info("Downloaded %s", filename)

    logging.info("Downloaded %d files to %s", len(FILES), data_dir)



def upload_outputs(output_dir: Path, github_username: str) -> None:
    """Task 7 (extra credit): Upload Parquet outputs to Azure and verify the round-trip."""
    if not github_username or github_username == "<halyna1995>":
        raise ValueError("Set GITHUB_USERNAME to your GitHub username before running the pipeline.")

    output_dir = Path(output_dir)
    container_name = f"week4-{github_username.lower()}-outputs"

    # EXTRA CREDIT — implement this after Tasks 2–6 are working.

    credential = DefaultAzureCredential()
    service = BlobServiceClient(account_url=ACCOUNT_URL, credential=credential)
    container = service.get_container_client(container_name)

    try:
        container.create_container()
        logging.info("Created container %s.", container_name)
    except ResourceExistsError:
        logging.info("Container %s already exists.", container_name)
    except AzureError as error:
        raise RuntimeError(f"Could not create Azure container {container_name}.") from error

    for parquet_file in output_dir.glob("*.parquet"):
        blob_client = container.get_blob_client(parquet_file.name)
        with open(parquet_file, "rb") as f:
            blob_client.upload_blob(f, overwrite=True)
        logging.info("Uploaded %s to container %s", parquet_file.name, container_name)

    local_customer_summary = output_dir / "customer_summary.parquet"
    blob_client = container.get_blob_client("customer_summary.parquet")
    remote_customer_summary = pd.read_parquet(io.BytesIO(blob_client.download_blob().readall()))
    assert len(remote_customer_summary) == len(local_customer_summary)

    logging.info(
        "Azure round-trip verified for customer_summary.parquet: %s rows.",
        len(remote_customer_summary),
    )
