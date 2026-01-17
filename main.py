"""Entry point."""

from datetime import datetime

from src.config import ConfigurationError, get_env_vars
from src.drive import DriveBackupService
from src.storage import StorageClient


def main() -> None:
    """Main file."""
    # Get env vars
    try:
        config = get_env_vars()
    except ConfigurationError as ce:
        print(f'Error getting env vars: {ce}')

    # Setup services
    print('Starting Backup Job...')
    storage_system = StorageClient(config.bucket_name)
    backup_system = DriveBackupService(storage_system)

    # Define Backup root
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')
    root_folder = f'backup_{timestamp}'

    # Start recursion
    try:
        backup_system.backup_recursive(config.source_folder_id, root_folder)
        print('Backup Job Completed Successfully.')
    except Exception as e:
        print(f'An exception occured: {e}')
        raise e  # Re-raise so Cloud Run knows it failed:
    else:
        print('Backup Job completed')


if __name__ == '__main__':
    main()
