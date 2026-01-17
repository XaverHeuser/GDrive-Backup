"""File for config stuff."""

import os
from typing import NamedTuple


class ConfigurationError(RuntimeError):
    """Raised when required configuration is missing."""


class AppConfig(NamedTuple):
    bucket_name: str
    source_folder_id: str


def get_env_vars() -> AppConfig:
    bucket_name = os.environ['BUCKET_NAME']
    source_folder_id = os.environ['FOLDER_ID']

    missing: list[str] = []
    if not bucket_name:
        missing.append('BUCKET_NAME')
    if not source_folder_id:
        missing.append('FOLDER_ID')

    if missing:
        raise ConfigurationError(
            f'Missing required environment variables: {", ".join(missing)}'
        )

    return AppConfig(bucket_name=bucket_name, source_folder_id=source_folder_id)
