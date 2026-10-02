CREATE TABLE IF NOT EXISTS transactions (
 transaction_id TEXT PRIMARY KEY, customer_id TEXT NOT NULL,
 timestamp TEXT NOT NULL, amount REAL NOT NULL CHECK(amount>0),
 payload TEXT NOT NULL, result TEXT NOT NULL,
 risk_score REAL NOT NULL CHECK(risk_score BETWEEN 0 AND 100),
 decision TEXT NOT NULL CHECK(decision IN ('approve','verify','review')),
 model_version TEXT NOT NULL, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_customer_time ON transactions(customer_id,timestamp);
CREATE TABLE IF NOT EXISTS feedback (
 transaction_id TEXT PRIMARY KEY REFERENCES transactions(transaction_id),
 is_fraud INTEGER NOT NULL CHECK(is_fraud IN (0,1)),
 reviewed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
