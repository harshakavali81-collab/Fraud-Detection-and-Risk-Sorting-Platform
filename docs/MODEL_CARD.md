# Model card

Purpose: demonstrate transaction risk scoring on synthetic data, not authorize real payments.
Data: 12,000 generated transactions, 150 possible customers, Jan 2026 UTC, INR amounts; seed 42. Source: src/generate.py. Fraud rate: 1.25%.
Inputs: log amount, amount relative to preceding 24-hour mean, preceding one-hour count, new device relative to all earlier customer events, UTC night indicator, country mismatch. Country mismatch is not evidence of criminal behavior.
Targets: synthetic sampled fraud outcomes. Labels are excluded from features and online requests.
Training: first 60%. Validation: next 20%. Test: final 20%. Preprocessing fits on training only. Historical features can use earlier events across split boundaries, never their labels or future events.
Candidates: standardized Logistic Regression and Random Forest. Select by validation average precision. No resampling is used.
Policy: verify threshold 0.025000 maximizes validation F2 over a fixed grid. Review threshold 0.057340 is the higher of validation 95th percentile and verify+0.001. The 5% queue target is approximate, validation-only, and not a future capacity guarantee.
Scores: model output multiplied by 100, rounded for display only; decisions use the unrounded value. Not calibrated probabilities. Reason flags are observed conditions, not causal model explanations or SHAP values.
Limitations: synthetic label mechanism, small positive test count (30), no uncertainty intervals, weak alert precision, no real-world validation. Repeatedly tuning against this test set would invalidate the evaluation.
Operations: joblib artifact bundles schema and thresholds. Engine loads one artifact at startup. Feedback is stored, never automatically used for retraining. Retrain offline and restart after reviewing metrics. Version synthetic-v1 is a demo label; production needs immutable version IDs and registry approvals.
