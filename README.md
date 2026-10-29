# Real-Time Fraud Detection and Risk Scoring Platform

Python, SQL, machine learning, FastAPI and Streamlit portfolio project for Kavali Harshavardhan.

[Setup](#local-installation--setup-guide) · [Architecture](#architecture--system-design-diagram) · [Detailed guide](PROJECT_GUIDE.md) · [Repository standard](docs/REPOSITORY_STANDARD.md)

## Visuals

![Architecture](<docs/architecture.png>)

Existing project visual; diagrams and illustrative graphics are not evidence of a deployed application.

## Live Link / Demo

Run the local demo using the setup guide below. No public deployment URL has been verified for this documentation update.

## Key Features

| Folder/file | Purpose |
|---|---|
| `src/generate.py` | Reproducible 12,000-row synthetic transaction generator |
| `src/features.py` | Shared point-in-time feature logic |
| `src/train.py` | Chronological split, two models, validation thresholds, holdout evaluation |
| `src/engine.py` | Persistent SQLite scoring, idempotency, history and feedback |
| `src/api.py` | Validated FastAPI endpoints |
| `src/simulate.py` | Transaction replay through HTTP |
| `dashboard.py` | Automatically refreshed review dashboard and manual scoring |
| `src/kafka_bridge.py` | Optional Kafka producer/consumer bridge |
| `src/monitor.py` | Reference-versus-current feature shift report |
| `sql/` | Schema and analytical queries |
| `notebooks/EDA.ipynb` | Re-runnable exploratory analysis |
| `reports/` | Measured metrics, predictions, plots, test results and Excel workbook |
| `docs/` | Full guide, PDF, architecture, workflow, model card and interview notes |
| `tests/` | API and data-integrity tests |
| `compose.yaml` | Local API/dashboard containers with persistent state |

## Tech Stack

![Python](https://img.shields.io/badge/Python-334155?style=flat-square) ![FastAPI](https://img.shields.io/badge/FastAPI-334155?style=flat-square) ![Streamlit](https://img.shields.io/badge/Streamlit-334155?style=flat-square) ![scikit-learn](https://img.shields.io/badge/scikit--learn-334155?style=flat-square) ![Pandas](https://img.shields.io/badge/Pandas-334155?style=flat-square) ![NumPy](https://img.shields.io/badge/NumPy-334155?style=flat-square) ![SQL](https://img.shields.io/badge/SQL-334155?style=flat-square) ![Docker](https://img.shields.io/badge/Docker-334155?style=flat-square)

Dependency versions and optional packages are defined in the repository manifests.

## Architecture / System Design Diagram

[Architecture documentation / diagram](<docs/architecture.png>)

## Local Installation & Setup Guide

```bash
git clone https://github.com/harshakavali81-collab/Fraud-Detection-and-Risk-Sorting-Platform.git
cd Fraud-Detection-and-Risk-Sorting-Platform
```

Extract the ZIP, open the `fraud-platform` folder in VS Code and open its terminal.

```bash
python -m venv .venv
```

Windows PowerShell: `.venv\Scripts\Activate.ps1`. macOS/Linux: `source .venv/bin/activate`.

```bash
python -m pip install -r requirements.txt
python -m src.train
python -m pytest -q
python -m uvicorn src.api:app --host 127.0.0.1 --port 8000
```

Keep that terminal open. In a second activated terminal:

```bash
python -m streamlit run dashboard.py
```

Open http://localhost:8501. API documentation: http://localhost:8000/docs.
In a third activated terminal:

```bash
python -m src.simulate --count 300 --delay 0.1
```

The included dataset and model allow a quick demo. Always retrain after changing Python/scikit-learn versions. Load only trusted joblib files.

## Challenges & Solutions

**Repository organization:** this project uses `src/`. Keeping those paths stable avoids breaking imports, asset links and deployment commands while the documentation follows a shared format. Project-specific technical limitations and prior release evidence are retained in [Project guide](PROJECT_GUIDE.md).

## Future Improvements

- Capture a reproducible end-to-end demo with runtime versions and sample inputs.
- Expand regression checks for invalid inputs and documented edge cases.
- Record measured results, data provenance and deployment limitations alongside each release.

## Scope and supporting evidence

Python, SQL, machine learning, FastAPI and Streamlit portfolio project for Kavali Harshavardhan.

Scores incoming transactions and returns **approve**, **verify**, or **review**. These are demo decisions; no payment is actually approved or blocked.

## Repository Structure

| Location | Purpose |
| --- | --- |
| `src/` | Source modules |
| `tests/` | Tests |
| `docs/` | Documentation |
| `data/` | Data and samples |
| `sql/` | SQL schema and analysis |
| `scripts/` | Automation scripts |
| `.github/` | Issue forms, PR template and automated checks |

[Complete file inventory and workflow](docs/REPOSITORY_STANDARD.md). Runtime entry points retain their existing paths.

## Workflow & Tracking

Use the [bug and feature forms](https://github.com/harshakavali81-collab/Fraud-Detection-and-Risk-Sorting-Platform/issues/new/choose) to define work with acceptance criteria. Keep tasks in Todo → In progress → Review → Done, and link a pull request with `Closes #<number>`. See [the maintenance workflow](docs/REPOSITORY_STANDARD.md#workflow).

## License

Original project software is available under the [MIT License](LICENSE). See [licensing scope](docs/LICENSING.md) for third-party and data exclusions.

