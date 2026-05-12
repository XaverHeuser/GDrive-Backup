"""Handles everything related to the destination (GCS Bucket)"""

import io

from google.cloud import storage


class StorageClient:
    def __init__(self, bucket_name: str):
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)

    def file_exists(self, blob_path: str) -> bool:
        """Checks if file already exists to avoid redundant uploads."""
        blob = self.bucket.blob(blob_path)
        return bool(blob.exists())

    def upload_from_handle(
        self, file_handle: io.IOBase, blob_path: str, content_type: str | None = None
    ) -> None:
        """Uploads from a file handle with restricted memory buffering."""
        blob = self.bucket.blob(blob_path)

        # Configure chunk size (e.g., 32MB) to prevent large memory buffers during upload
        blob.chunk_size = 32 * 1024 * 1024

        file_handle.seek(0)
        blob.upload_from_file(file_handle, content_type=content_type)

        print(f'Uploaded: {blob_path}')
