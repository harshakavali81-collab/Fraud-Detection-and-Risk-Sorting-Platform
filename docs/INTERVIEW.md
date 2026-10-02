# Interview and presentation notes

## Two-minute explanation
I built a fraud-risk portfolio demo that accepts transactions through FastAPI, calculates features from earlier customer activity, scores them with a trained model and records a review decision in SQLite. A Streamlit dashboard displays recent events and lets an analyst record confirmed outcomes. I used a seeded synthetic dataset and chronological splits so that training precedes validation and test events. I compared Logistic Regression with Random Forest, selected by validation average precision and set thresholds on validation only. I tested duplicate replay, invalid payloads, out-of-order events and feedback. The main limitation is low precision on rare synthetic fraud. I would need real delayed labels, calibration and cost-based threshold evaluation before using it in a real setting.

## Questions to prepare
1. Why not accuracy? Most events are legitimate; an all-legitimate classifier can look accurate while missing every fraud event.
2. Why chronological split? Future transactions should not inform earlier predictions.
3. What is idempotency? A retry with the same transaction ID and payload returns the original result without inserting another event.
4. What is cold start? New customers or a new database have no historical activity. Defaults must be explicit.
5. Why are flags not explanations? They identify suspicious conditions but do not quantify each feature's model contribution.
6. How would you scale? Bounded recent-activity aggregates, persistent device state, Kafka partitions, a durable database, load tests and measured service-level objectives.
7. Why not auto-retrain from all reviews? Review selection is biased and labels may be wrong or delayed. Use label quality checks and independently evaluated retraining.

## Resume bullets (use after running and understanding the project)
- Built a Python fraud-risk demo with FastAPI, SQLite and Streamlit, including historical features, transaction replay, idempotent scoring and analyst feedback.
- Compared machine-learning models using chronological splits and average precision; documented synthetic-data limitations and validated API behavior through automated tests.

## Five-minute demo
0:00 Explain the business problem and synthetic data. 0:45 Show architecture. 1:30 Start simulation and dashboard. 2:30 Score one event and explain its flags. 3:15 Replay its ID and show unchanged result. 4:00 Explain precision/recall trade-off and limitations. 4:45 Open tests and GitHub structure.
