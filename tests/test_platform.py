import json
import pytest
from fastapi.testclient import TestClient
from src.api import app
from src.features import features
@pytest.fixture
def client(tmp_path,monkeypatch):
    monkeypatch.setenv('FRAUD_DB',str(tmp_path/'test.db'))
    with TestClient(app) as c:yield c
@pytest.fixture
def tx():return dict(transaction_id='t1',customer_id='c1',timestamp='2026-01-01T10:00:00Z',amount=100.0,device_id='d1',country='IN',home_country='IN')
def test_score_replay_conflict(client,tx):
    a=client.post('/score',json=tx);assert a.status_code==200
    assert 0<=a.json()['risk_score']<=100
    assert client.post('/score',json=tx).json()==a.json()
    assert len(client.get('/transactions').json())==1
    assert client.post('/score',json={**tx,'amount':101}).status_code==409
def test_out_of_order(client,tx):
    client.post('/score',json=tx)
    assert client.post('/score',json={**tx,'transaction_id':'t2','timestamp':'2025-12-31T10:00:00Z'}).status_code==409
@pytest.mark.parametrize('change',[{'amount':-1},{'timestamp':'2026-01-01T10:00:00'},{'country':'india'},{'extra':1}])
def test_bad_input(client,tx,change):assert client.post('/score',json={**tx,**change}).status_code==422
def test_feedback(client,tx):
    assert client.post('/feedback',json={'transaction_id':'none','is_fraud':1}).status_code==404
    client.post('/score',json=tx)
    assert client.post('/feedback',json={'transaction_id':'t1','is_fraud':1}).status_code==200
    assert client.post('/feedback',json={'transaction_id':'t1','is_fraud':3}).status_code==422
def test_no_future_leakage(tx):
    future={**tx,'timestamp':'2027-01-01T10:00:00Z','amount':99999}
    assert features(tx,[future])==features(tx,[])
def test_history_features(tx):
    past={**tx,'timestamp':'2026-01-01T09:30:00Z','amount':25,'device_id':'old'}
    f=features(tx,[past]);assert f['count_1h']==1 and f['amount_ratio']==4 and f['new_device']==1

def test_online_offline_feature_parity(tmp_path):
    import pandas as pd
    from src.engine import Engine
    from src.features import FEATURES
    engine=Engine(tmp_path/'parity.db')
    rows=pd.read_csv('data/transactions.csv').head(20).drop(columns=['is_fraud']).to_dict('records')
    expected=pd.read_csv('data/features.csv').head(20)
    for i,tx in enumerate(rows):
        result=engine.score(tx)
        prob=engine.artifact['model'].predict_proba(expected.iloc[[i]][FEATURES])[0,1]
        assert result['risk_score']==round(prob*100,2)

def test_concurrent_duplicate(tmp_path,tx):
    from concurrent.futures import ThreadPoolExecutor
    from src.engine import Engine
    engine=Engine(tmp_path/'concurrent.db')
    with ThreadPoolExecutor(max_workers=4) as pool:
        results=list(pool.map(lambda _:engine.score(tx),range(4)))
    assert all(r==results[0] for r in results)
    assert len(engine.recent())==1
