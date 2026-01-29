# GDrive-Backup

A Python-based utility to backup specific folders from Google Drive to Google Cloud Storage (GCS). This solution is Dockerized and designed to be deployed via Google Cloud Build/Cloud Run or scheduled via Cloud Scheduler.

## 🚀 Features

- **Automated Backup**: Recursively copies files from a source Google Drive folder.
- **Cloud Storage Integration**: Uploads files directly to a specified GCS Bucket.
- **Docker Ready**: Includes a `Dockerfile` for easy containerization.
- **CI/CD Integrated**: Includes `cloudbuild.yaml` for Google Cloud Build pipelines.
- **Jupyter Support**: Includes notebooks for data exploration or testing.

## 🛠 Prerequisites

Before running this script, you need:

1. **Google Cloud Project**: A valid GCP project.
2. **Service Account**:
    - Create a Service Account in IAM.
    - Download the JSON Key file.
    - Grant the Service Account the **Storage Object Admin** role.
3. **Google Drive API**: Enable the Drive API in your GCP project.
4. **Drive Permissions**: Share the target Google Drive folder with the Service Account email address (e.g., `my-app@project-id.iam.gserviceaccount.com`).

## ⚙️ Configuration

The application relies on environment variables. You can set these in a `.env` file for local development or in your Cloud Run/Build configuration.

| Variable | Description | Example |
| :--- | :--- | :--- |
| `PROJECT_ID` | Your Google Cloud Project ID | `my-backup-project` |
| `SOURCE_FOLDER_ID` | The ID of the Google Drive folder to backup | `1A2B3C...` |
| `BUCKET_NAME`| The name of the GCS bucket | `my-drive-backups` |

## 💻 Local Installation & Usage

1. **Clone the repository**

    ```bash
    git clone [https://github.com/XaverHeuser/GDrive-Backup.git](https://github.com/XaverHeuser/GDrive-Backup.git)
    cd GDrive-Backup
    ```

2. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3. **Setup Google Cloud environment**s

4. **Run the Script**

    ```bash
    python main.py
    ```

## ☁️ Deployment

### Google Cloud Build

This project includes a `cloudbuild.yaml`. To trigger a build:

```bash
gcloud builds submit --config cloudbuild.yaml .
```

### Cloud Run & Scheduler

To set up an automated schedule:

1. Deploy the image to **Cloud Run.**

2. Create a **Cloud Scheduler** job to trigger the Cloud Run service endpoint (e.g., every night at 3 AM).

### Enhancement

Load data from Google Cloud Storage to local PC:

1. Open Google Cloud SDK Shell
2. Navigate to the target folder
3. Enter the following command:
   ```bash
   gsutil -m cp -r "gs://gdrive-backup-2026/backup_{date}" .
   ```
   date = YYYY-MM-DD_HH-mm
   

### 📂 Project Structure

- src/: Source code modules.
- notebooks/: Jupyter notebooks for testing API connections or data analysis.
- main.py: Entry point for the backup script.
- Dockerfile: Container definition.

### 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
