"""Handles the recursion logic and data fetching."""

import io
from typing import TypedDict

import google.auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

from src.storage import StorageClient


class ExportConfig(TypedDict):
    mime: str
    ext: str


# Configuration: Which Google-format belongs wo which Office-format
EXPORT_MAPPING: dict[str, ExportConfig] = {
    'application/vnd.google-apps.document': {
        'mime': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'ext': '.docx',
    },
    'application/vnd.google-apps.spreadsheet': {
        'mime': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'ext': '.xlsx',
    },
    'application/vnd.google-apps.presentation': {
        'mime': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        'ext': '.pptx',
    },
}


class DriveBackupService:
    def __init__(self, storage_service: StorageClient):
        # Authenticate using default credentials (works locally & on Cloud Run)
        creds, _ = google.auth.default(
            scopes=['https://www.googleapis.com/auth/drive.readonly']
        )
        self.service = build('drive', 'v3', credentials=creds, cache_discovery=False)
        self.storage = storage_service

    def backup_recursive(self, folder_id: str, current_path: str) -> None:
        """Recursively scans folders and triggers backup for files."""
        print(f'Scanning Folder: {current_path}')

        page_token: str | None = None

        while True:
            # Query items in folder
            query = f"'{folder_id}' in parents and trashed = false"
            results = (
                self.service.files()
                .list(
                    q=query,
                    fields='nextPageToken, files(id, name, mimeType)',
                    pageToken=page_token,
                )
                .execute()
            )

            # Process Items
            items = results.get('files', [])
            for item in items:
                self._process_item(item, current_path)

            # Check if there is another page with results
            page_token = results.get('nextPageToken')
            if not page_token:
                break

    def _process_item(self, item: dict[str, str], current_path: str) -> None:
        """Decides if it is a folder (recursion) or a file (upload)"""
        file_id: str = item['id']
        name: str = item['name'].replace('/', '_')  # Sanitize filename
        mime: str = item['mimeType']

        full_path = f'{current_path}/{name}'

        # CASE 1: Folder -> Recurse
        if mime == 'application/vnd.google-apps.folder':
            self.backup_recursive(file_id, full_path)
        # CASE 2: File -> Download & Upload
        else:
            self._handle_file(file_id, name, mime, full_path)

    def _handle_file(self, file_id: str, name: str, mime: str, full_path: str) -> None:
        """Handles conversion and upload for files"""
        export_config = EXPORT_MAPPING.get(mime)

        # Set target filename and mime-type
        if export_config:
            # If it is a google-format -> Append ending
            target_path = full_path + export_config['ext']
            target_mime = export_config['mime']
            print(f'Convert to Office-format  ({export_config["ext"]}): {name}')
            request = self.service.files().export_media(
                fileId=file_id, mimeType=target_mime
            )
            # is_conversion = True
        else:
            if mime.startswith('application/vnd.google-apps'):
                print('Skipping unsupported Google type: %s (%s)', name, mime)
                return

            # If it is a regular format -> No changes
            target_path = full_path
            target_mime = mime

            print(f'Download: {name}')
            request = self.service.files().get_media(fileId=file_id)
            # is_conversion = False

        # Check if file already in bucket
        if self.storage.file_exists(target_path):
            print(f'Skip (File already exists): {target_path}')
            return

        # Prepare buffer
        fh = io.BytesIO()

        try:
            # Execute Downloader
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                _, done = downloader.next_chunk()

            # Upload file in bucket
            self.storage.upload_stream(fh, target_path, content_type=target_mime)

        except Exception:
            print('Failed processing file: %s', name)
            raise
