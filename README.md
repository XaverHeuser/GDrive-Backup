# GDrive-Backup

A memory-optimized, containerized Python utility designed to recursively backup specific Google Drive directories directly to a Google Cloud Storage (GCS) target bucket.

[![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI Pipeline](https://img.shields.io/badge/CI-Ruff%20%7C%20Mypy%20%7C%20Bandit-brightgreen.svg)](https://github.com/XaverHeuser/GDrive-Backup/actions)
[![Docker Built](https://img.shields.io/badge/Docker-Ready-blue.svg)](Dockerfile)

---

## 🚀 Features

- **Automated Directory Backup**: Recursively traverses nested Google Drive folder hierarchies to clone objects down to a defined storage location.
- **Dynamic Format Conversion**: Automatically transforms proprietary Google Workspace application binaries (Docs, Sheets, Slides) into standard open-source formats (`.docx`, `.xlsx`, `.pptx`) on-the-fly during transmission.
- **Enterprise Memory Safety**: Implements a data streaming pipeline utilizing hybrid `SpooledTemporaryFile` configurations alongside strict object chunking allocations (32MB) to handle massive file payloads without memory exhaustion.
- **Cloud-Native Deployment**: Shipped with complete `Dockerfile` configurations and automated Google Cloud Build pipelines (`cloudbuild.yaml`) tailored for Cloud Run and Cloud Scheduler orchestration.
- **Local Sandbox Utilities**: Includes analytical Jupyter notebooks to explicitly verify API handshake endpoints and check metadata structures during development environments.

---

## 🛠 Prerequisites & IAM Configuration

Before launching execution layers, verify your GCP and Google Workspace environments comply with the following access management configurations:

1. **Google Cloud Project**: An active GCP Project ID with billing enabled.
2. **Service Account Setup**:
   - Create a dedicated IAM Service Account (e.g., `backup-runner@your-project.iam.gserviceaccount.com`).
   - Generate and download a local authentication cryptographic credential structure via a JSON Key file (only required for local testing environments).
   - Grant the Service Account the **Storage Object Admin** role (`roles/storage.objectAdmin`) over your destination storage infrastructure.
3. **Target API Activation**: Enable the **Google Drive API** and the **Google Cloud Storage API** within the Google Cloud API Library console dashboard.
4. **Domain/Drive Share Delegation**: Grant the generated Service Account IAM email identity standard **Viewer** permissions explicitly on your target parent Google Drive directory.

---

## ⚙️ Configuration & Environment Variables

The backup orchestrator parses configuration values straight out of runtime environment declarations. Ensure the following specific keys are initialized:

| Environment Variable | Description | Runtime Context Sample Value |
| :--- | :--- | :--- |
| `PROJECT_ID` | Main targeting Google Cloud Platform Project identifier | `my-backup-project-484609` |
| `FOLDER_ID` | The alphanumeric unique identifier found in the URL string of the root Google Drive source folder | `1A2B3C4D5E6F7G8H9I0J...` |
| `BUCKET_NAME` | The absolute target destination name of the Google Cloud Storage bucket | `my-drive-backups-bucket` |

---

## 💻 Local Installation & Usage

### 1. Initialize Workspace Environment

```bash
# Clone repository source files
git clone [https://github.com/XaverHeuser/GDrive-Backup.git](https://github.com/XaverHeuser/GDrive-Backup.git)
cd GDrive-Backup

# Setup isolated Python virtual environment framework
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Dependency Management Execution

```bash
# Upgrade core package managers to locked configurations
python -m pip install --upgrade pip==26.1.1

# Deploy core execution frameworks
python -m pip install -r requirements.txt

# (Optional) Deploy code analysis tools, linters, and testing engines
python -m pip install -r requirements-dev.txt
```

### 3. Local Runtime Authentication & Launch

For local desktop debugging operations, set up Application Default Credentials (ADC) or explicitly point your shell runtime to your downloaded Service Account key file:

```bash
# Export credential structures and targeted configurations
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
export BUCKET_NAME="your-gcs-bucket-name"
export FOLDER_ID="your-google-drive-folder-id"

# Initiate the extraction backup script
python main.py
```

## ☁️ Production Deployment Model

### Infrastructure & Deployment Architecture

The following diagram illustrates how the component services interact across the local CI/CD environment, Google Cloud Platform, and Google Workspace boundaries during an automated backup execution window:

[![GDrive Backup Architecture Diagram](https://img.plantuml.biz/plantuml/svg/VLJlRzem4FsEbF_XngGDfD5AwxT-c0e9CBHsHOHEcZG9cUG87euTsGujc_g_xsm72lsnVFBPzvxlthtuobYcRLqA62UQRt4nODcchXPzdQsvnSpM6gFMExl64g4IZCkePJPSLaop4Z9LLagYjAdT2GHD-KmMWX1HYsLMQMWdk4MXAjHjO0OeScUPK7KExR5Ib0onZwQ2sPNIPHl-HYsWxq0ExP2HPclCQz5G7I9uVysBjHs86jy0pce9dKHb6qgEbRJK1UgkP_49xZoGZ3MYt1VmZAias5cryx0RByGhIKPdPvcIAru4UhzyCpDtal-I7IzzK3v5lUKPXkhyVhFp9eaXdLdXQDAmYWMdmy3GR9rmFBwGwMGGWvgB_4aS7nxaORi0pfbbIsOGsdrj-Og63JCikB4w2BGF_WCykJGzD36EKog1PjLquE90yXE5KFTHwz5Pw0LFqcYPgbfd22CbylsGWxKRbYcN6qVm4UB9UPp0o7EICQ6dUr-EUxw4kUP5WTh0qcziEGDlNH-UxLWfejOHe9SJmQ7pIvZMPeqqnU2yIKaDXfk73vZLbYlPtFxavTw-1EV9em9-goLqlixdKvZUflFpFQ0RjPmL0ynxZK0pPBc1eTnohMJf1lo3QSwMWchf3ExYRyFvudl_PlW9HhVNoN2sc2J7FCUc8xQ9v9OpmVyG-WDmkLKRMYt3Cq5_VAqDvNUE6KvDzupZnAHEZfFx7BmPLzF8-V2XKjeQM77VG3ZiJoUmlUY-Wdvn-PGPGq1d6A318BrRRf1ffPJ07EP8lu5cDB0HTo_NCxmlY2nu2NULK4xOfL1B0yPrZc87dNXTomqOQWukFjyCkgwdAvGvFQh_0000)](https://editor.plantuml.com/uml/VLJlRzem4FsEbF_XngGDfD5AwxT-c0e9CBHsHOHEcZG9cUG87euTsGujc_g_xsm72lsnVFBPzvxlthtuobYcRLqA62UQRt4nODcchXPzdQsvnSpM6gFMExl64g4IZCkePJPSLaop4Z9LLagYjAdT2GHD-KmMWX1HYsLMQMWdk4MXAjHjO0OeScUPK7KExR5Ib0onZwQ2sPNIPHl-HYsWxq0ExP2HPclCQz5G7I9uVysBjHs86jy0pce9dKHb6qgEbRJK1UgkP_49xZoGZ3MYt1VmZAias5cryx0RByGhIKPdPvcIAru4UhzyCpDtal-I7IzzK3v5lUKPXkhyVhFp9eaXdLdXQDAmYWMdmy3GR9rmFBwGwMGGWvgB_4aS7nxaORi0pfbbIsOGsdrj-Og63JCikB4w2BGF_WCykJGzD36EKog1PjLquE90yXE5KFTHwz5Pw0LFqcYPgbfd22CbylsGWxKRbYcN6qVm4UB9UPp0o7EICQ6dUr-EUxw4kUP5WTh0qcziEGDlNH-UxLWfejOHe9SJmQ7pIvZMPeqqnU2yIKaDXfk73vZLbYlPtFxavTw-1EV9em9-goLqlixdKvZUflFpFQ0RjPmL0ynxZK0pPBc1eTnohMJf1lo3QSwMWchf3ExYRyFvudl_PlW9HhVNoN2sc2J7FCUc8xQ9v9OpmVyG-WDmkLKRMYt3Cq5_VAqDvNUE6KvDzupZnAHEZfFx7BmPLzF8-V2XKjeQM77VG3ZiJoUmlUY-Wdvn-PGPGq1d6A318BrRRf1ffPJ07EP8lu5cDB0HTo_NCxmlY2nu2NULK4xOfL1B0yPrZc87dNXTomqOQWukFjyCkgwdAvGvFQh_0000)

### Automated Google Cloud Build Execution

The infrastructure framework provides a managed template parsing a unified container build layout. Dispatch the build command straight into Cloud Build environments using the Google Cloud SDK CLI framework:

### Google Cloud Build

This project includes a `cloudbuild.yaml`. To trigger a build:

```bash
gcloud builds submit --config cloudbuild.yaml .
```

### Serverless Cloud Run Hosting & Cron Job Scheduling

To establish zero-maintenance serverless execution on a daily cron loop:

1. **Deploy Containerized Target:** Instatiate a new serverless instance inside Cloud Run Job platforms targeting the newly compiled artifact registry URL image path. Set the execution timeout boundaries to match your data size specifications.

2. **Setup Cloud Scheduler Triggers:** Establish an encrypted Cloud Scheduler job utilizing unified cron configuration syntaxes (e.g., 0 3 * * * for nightly execution loops at 3:00 AM) firing an authenticated OIDC service token target ping directly against your Cloud Run service URL endpoint.

## 🔒 Memory Safety & Production Guardrails

To operate cleanly under serverless run environments like Cloud Run (which feature tight runtime memory restrictions), the utility contains specific performance guardrails:

- **Redundant Check Prevention:** Every object undergoes an index comparison evaluation prior to initiating network queries. If a file path matches existing historical blob configurations inside the bucket, operations drop execution immediately to mitigate api call overruns.

- **Dynamic Memory Spooling:** Payload handling maps streams through a maximum 50MB allocation bracket of physical RAM memory before automatically spooling excessive overflows seamlessly into transient block files via tempfile.SpooledTemporaryFile.

- **Stream Buffering:** Data pushes explicitly bind upload loops into standard 32MB payload packets (blob.chunk_size = 32 * 1024 * 1024) to minimize local buffering.

- **Active Memory Sweeps:** The background orchestrator forces system garbage collection (gc.collect()) systematically at fixed index loops (every 20 items processed) to release unallocated blocks and flatten memory leaks.

## 📂 Repository Structure

```text
├── .github/                 # Automated validation workflows & dependency maintenance engines
│   └── workflows/
│       └── ci-pipeline.yml  # Comprehensive Continuous Integration pipeline definitions
├── notebooks/               # Local diagnostic exploratory environments and integration sandboxes
├── src/                     # Core operational package definitions
│   ├── config.py            # Environment validation checks and parsing rules
│   ├── drive.py             # Recursive Google Drive traversal logic and stream download protocols
│   └── storage.py           # Google Cloud Storage backend ingestion client interfaces
├── main.py                  # Standard main execution gateway routine
├── Dockerfile               # Production container image manifest rules
└── cloudbuild.yaml          # Google Cloud Build compilation pipelines
```

## ♻️ Load data from Google Cloud Storage to local PC

1. Open Google Cloud SDK Shell
2. Navigate to the target folder
3. Enter the following command:

   ```bash
   gsutil -m cp -r "gs://gdrive-backup-2026/backup_{date}" .
   ```

   *date format equals: YYYY-MM-DD_HH-mm*

## 📄 License
Distributed directly under the terms of the open-source MIT License guidelines. See the standard accompanying LICENSE text metadata file for deep details.
