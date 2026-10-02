"""Synthetic data only. Labels are sampled from an artificial risk process."""
import json
from pathlib import Path
from datetime import datetime, timedelta, timezone
import numpy as np
import pandas as pd
from src.features import features

def generate(n=12000, seed=42):
    rng=np.random.default_rng(seed); history={}; rows=[]
    start=datetime(2026,1,1,tzinfo=timezone.utc)
    for i in range(n):
        c=f'C{rng.integers(1,151):04d}'
        amount=round(float(np.clip(rng.lognormal(7,1.2),1,250000)),2)
        tx=dict(transaction_id=f'T{i:06d}', customer_id=c,
            timestamp=(start+timedelta(seconds=i*30)).isoformat(), amount=amount,
            device_id=c+('-new'+str(i) if rng.random()<.09 else '-phone'),
            country='US' if rng.random()<.08 else 'IN', home_country='IN')
        f=features(tx,history.get(c,[]))
        logit=-5.6+1.7*f['new_device']+1.8*f['foreign']+.6*f['night']+1.2*(amount>6000)+.8*(f['amount_ratio']>4)+.5*(f['count_1h']>2)
        label=int(rng.random()<1/(1+np.exp(-logit)))
        rows.append({**tx,'is_fraud':label});history.setdefault(c,[]).append(tx)
    return pd.DataFrame(rows)
if __name__=='__main__':
    Path('data').mkdir(exist_ok=True)
    df=generate();df.to_csv('data/transactions.csv',index=False)
    print(f'Generated {len(df)} synthetic transactions; fraud rate {df.is_fraud.mean():.2%}')
