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

    def upload_stream(
        self, stream: io.BytesIO, blob_path: str, content_type: str | None = None
    ) -> None:
        """Uploads a memory stream to GCS."""
        blob = self.bucket.blob(blob_path)
        # Rewind stream to beginning before reading
        stream.seek(0)
        blob.upload_from_file(stream, content_type=content_type)
        print(f'Uploaded: {blob_path}')
