-- Alert volume and amount in INR. Queue membership is not confirmed fraud.
SELECT decision,COUNT(*) AS transactions,SUM(amount) AS amount_inr,AVG(risk_score) AS mean_risk FROM transactions GROUP BY decision;
-- Confirmed outcomes only. Unreviewed transactions must not become negative labels.
SELECT t.decision,COUNT(*) AS reviewed,SUM(f.is_fraud) AS confirmed_fraud
FROM transactions t JOIN feedback f USING(transaction_id) GROUP BY t.decision;
-- Daily UTC activity
SELECT substr(timestamp,1,10) AS day_utc,COUNT(*) AS transactions FROM transactions GROUP BY day_utc ORDER BY day_utc;
