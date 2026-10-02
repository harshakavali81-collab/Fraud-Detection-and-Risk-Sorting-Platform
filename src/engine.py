import json, sqlite3, time
from pathlib import Path
import joblib
import pandas as pd
from src.features import features, timestamp
class Conflict(ValueError): pass
class Engine:
    def __init__(self, db='data/live.db', model='models/fraud_model.joblib'):
        self.db=str(db);self.artifact=joblib.load(model)
        Path(self.db).parent.mkdir(parents=True,exist_ok=True)
        with self.connect() as conn: conn.executescript(Path('sql/schema.sql').read_text())
    def connect(self):
        conn=sqlite3.connect(self.db,timeout=30)
        conn.execute('PRAGMA foreign_keys=ON');return conn
    def score(self, tx):
        started=time.perf_counter();tx=dict(tx)
        tx['timestamp']=timestamp(tx['timestamp']).isoformat();payload=json.dumps(tx,sort_keys=True)
        with self.connect() as conn:
            conn.execute('BEGIN IMMEDIATE')
            old=conn.execute('SELECT payload,result FROM transactions WHERE transaction_id=?',(tx['transaction_id'],)).fetchone()
            if old:
                if old[0]!=payload:raise Conflict('Transaction ID already used with a different payload')
                return json.loads(old[1])
            history=[json.loads(r[0]) for r in conn.execute('SELECT payload FROM transactions WHERE customer_id=? ORDER BY timestamp',(tx['customer_id'],))]
            if history and timestamp(tx['timestamp'])<=timestamp(history[-1]['timestamp']):
                raise Conflict('Send transactions in strictly increasing time order per customer')
            f=features(tx,history)
            prob=float(self.artifact['model'].predict_proba(pd.DataFrame([f])[self.artifact['features']])[0,1])
            decision='review' if prob>=self.artifact['review_threshold'] else 'verify' if prob>=self.artifact['verify_threshold'] else 'approve'
            reasons=[name for name,flag in [('new_device',f['new_device']),('foreign_country',f['foreign']),('amount_above_recent_average',f['amount_ratio']>4),('frequent_transactions',f['count_1h']>2),('night_UTC',f['night'])] if flag]
            result=dict(transaction_id=tx['transaction_id'],risk_score=round(prob*100,2),decision=decision,
                reason_flags=reasons,model_version=self.artifact['version'],scoring_ms=round((time.perf_counter()-started)*1000,3))
            conn.execute('INSERT INTO transactions(transaction_id,customer_id,timestamp,amount,payload,result,risk_score,decision,model_version) VALUES (?,?,?,?,?,?,?,?,?)',
                (tx['transaction_id'],tx['customer_id'],tx['timestamp'],tx['amount'],payload,json.dumps(result),result['risk_score'],decision,result['model_version']))
            return result
    def recent(self,limit=200):
        with self.connect() as c:
            return [dict(zip(['transaction_id','customer_id','timestamp','amount','risk_score','decision'],r)) for r in c.execute('SELECT transaction_id,customer_id,timestamp,amount,risk_score,decision FROM transactions ORDER BY timestamp DESC LIMIT ?',(limit,))]
    def feedback(self, transaction_id, is_fraud):
        with self.connect() as c:
            if not c.execute('SELECT 1 FROM transactions WHERE transaction_id=?',(transaction_id,)).fetchone():raise KeyError(transaction_id)
            c.execute('INSERT INTO feedback(transaction_id,is_fraud) VALUES (?,?) ON CONFLICT(transaction_id) DO UPDATE SET is_fraud=excluded.is_fraud,reviewed_at=CURRENT_TIMESTAMP',(transaction_id,is_fraud))
