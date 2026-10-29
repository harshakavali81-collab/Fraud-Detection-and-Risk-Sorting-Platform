# Repository standard

## Layout

This repository keeps its working source paths. A shared portfolio structure does not require moving a React application, Python package, BI workbook or Verilog project into identical runtime directories.

| Area | Convention |
| --- | --- |
| Landing page | `README.md`: purpose, visuals, demo, features, stack, architecture, setup, tradeoffs and roadmap |
| Detailed reference | `PROJECT_GUIDE.md`: retained project-specific explanation and historical release notes |
| Documentation | `docs/`: design, inventory, reproduction and evidence |
| Work intake | `.github/ISSUE_TEMPLATE/`: bug and feature forms |
| Review | `.github/PULL_REQUEST_TEMPLATE.md`: linked issue, behavior and validation |
| Automation | `.github/workflows/portfolio-docs.yml`: README section and local-link checks |
| Source and tests | Existing project-specific paths listed below; no empty source/test placeholders |

## Workflow

1. Open an issue describing the user problem and measurable acceptance criteria.
2. Add it to a GitHub Project with Todo, In progress, Review and Done states when a board is configured.
3. Use a focused branch and meaningful commits, such as `docs: correct local setup paths` or `fix(api): reject malformed input`.
4. Run the project's documented checks and `python scripts/check_portfolio_docs.py`.
5. Open a pull request with actual validation results and `Closes #<issue-number>`.
6. Merge after review; record release evidence and update the issue/board.

Board creation, profile pins, repository social previews and milestone settings require account-level configuration. This file does not claim those settings have been applied.

## Validation scope

The documentation check validates the landing-page headings and local link targets only. It does not execute models, certify test coverage, inspect Git history for secrets, verify external websites, or prove production readiness. Existing application workflows remain the source of runtime CI evidence.

Keep credentials in local environment variables. A gitignore rule does not remove secrets already tracked or committed. Use only permitted sample data in public demos.

## Inventory at standardization

The following are the pre-existing public project files. New standardization files are described above. Historical guides may mention external bundles that are not part of this list.

- [`Dockerfile`](<../Dockerfile>)
- [`README.md`](<../README.md>)
- [`compose.yaml`](<../compose.yaml>)
- [`dashboard.py`](<../dashboard.py>)
- [`data`](<../data>)
- [`data/features.csv`](<../data/features.csv>)
- [`data/transactions.csv`](<../data/transactions.csv>)
- [`docs`](<../docs>)
- [`docs/Fraud_Platform_Guide.pdf`](<../docs/Fraud_Platform_Guide.pdf>)
- [`docs/INTERVIEW.md`](<../docs/INTERVIEW.md>)
- [`docs/KAFKA.md`](<../docs/KAFKA.md>)
- [`docs/MODEL_CARD.md`](<../docs/MODEL_CARD.md>)
- [`docs/PROJECT_GUIDE.md`](<../docs/PROJECT_GUIDE.md>)
- [`docs/VALIDATION.md`](<../docs/VALIDATION.md>)
- [`docs/architecture.mmd`](<../docs/architecture.mmd>)
- [`docs/architecture.png`](<../docs/architecture.png>)
- [`docs/openapi.json`](<../docs/openapi.json>)
- [`docs/workflow.mmd`](<../docs/workflow.mmd>)
- [`models`](<../models>)
- [`models/fraud_model.joblib`](<../models/fraud_model.joblib>)
- [`notebooks`](<../notebooks>)
- [`notebooks/EDA.ipynb`](<../notebooks/EDA.ipynb>)
- [`reports`](<../reports>)
- [`reports/Dictionary_preview.png`](<../reports/Dictionary_preview.png>)
- [`reports/Fraud_Analytics.xlsx`](<../reports/Fraud_Analytics.xlsx>)
- [`reports/Holdout_preview.png`](<../reports/Holdout_preview.png>)
- [`reports/Summary_preview.png`](<../reports/Summary_preview.png>)
- [`reports/decisions.png`](<../reports/decisions.png>)
- [`reports/feature_shift.csv`](<../reports/feature_shift.csv>)
- [`reports/live_check.json`](<../reports/live_check.json>)
- [`reports/metrics.json`](<../reports/metrics.json>)
- [`reports/precision_recall.png`](<../reports/precision_recall.png>)
- [`reports/simulation.log`](<../reports/simulation.log>)
- [`reports/test_predictions.csv`](<../reports/test_predictions.csv>)
- [`reports/test_results.txt`](<../reports/test_results.txt>)
- [`requirements-kafka.txt`](<../requirements-kafka.txt>)
- [`requirements.txt`](<../requirements.txt>)
- [`scripts`](<../scripts>)
- [`scripts/build_guide.py`](<../scripts/build_guide.py>)
- [`sql`](<../sql>)
- [`sql/analysis.sql`](<../sql/analysis.sql>)
- [`sql/schema.sql`](<../sql/schema.sql>)
- [`src`](<../src>)
- [`src/__init__.py`](<../src/__init__.py>)
- [`src/api.py`](<../src/api.py>)
- [`src/engine.py`](<../src/engine.py>)
- [`src/features.py`](<../src/features.py>)
- [`src/generate.py`](<../src/generate.py>)
- [`src/kafka_bridge.py`](<../src/kafka_bridge.py>)
- [`src/monitor.py`](<../src/monitor.py>)
- [`src/simulate.py`](<../src/simulate.py>)
- [`src/train.py`](<../src/train.py>)
- [`tests`](<../tests>)
- [`tests/test_platform.py`](<../tests/test_platform.py>)
