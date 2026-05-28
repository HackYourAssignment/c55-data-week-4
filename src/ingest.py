"""Task 1: Download inputs from Azure. Task 7: Upload outputs back to Azure."""

import logging
from pathlib import Path
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

ACCOUNT_URL = "https://sthyfstudentsdemo.blob.core.windows.net"
SOURCE_CONTAINER = "week4-inputs"
FILES = ["messy_sales.csv", "messy_customers.csv"]


def download_inputs(data_dir: Path) -> None:
    """Task 1: Download input CSV files from Azure Blob Storage."""
    print("Initializing Azure credentials...")
    credential = DefaultAzureCredential()
    service = BlobServiceClient(account_url=ACCOUNT_URL, credential=credential)
    container = service.get_container_client(SOURCE_CONTAINER)

    data_dir.mkdir(parents=True, exist_ok=True)
    print(f"Target directory verified at: {data_dir.resolve()}")

    for name in FILES:
        print(f"Attempting to download {name}...")
        blob = container.get_blob_client(name)

        file_path = data_dir / name
        with open(file_path, "wb") as f:
            f.write(blob.download_blob().readall())

        logging.info("Downloaded %s to %s", name, file_path)
        print(f"Successfully downloaded: {name}")


if __name__ == "__main__":
    print("Script started...")
    target_directory = Path("./data")
    download_inputs(target_directory)
    print("Script finished.")


def upload_outputs(output_dir: Path, github_username: str) -> None:
    """Task 7 (extra credit): Upload Parquet outputs to Azure and verify the round-trip."""
    container_name = f"week4-{github_username}"

    # EXTRA CREDIT — implement this after Tasks 2–6 are working.
    # TODO: Create a BlobServiceClient using DefaultAzureCredential and ACCOUNT_URL.
    # TODO: Get (or create) the container named container_name.
    # TODO: Upload every .parquet file in output_dir to the container.
    # TODO: Download customer_summary.parquet back and assert its row count matches the local file.
    # TODO: Log the container name and number of files uploaded.
    raise NotImplementedError("Task 7: implement upload_outputs")
