import os
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Literal
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator, ConfigDict
from src.engine import Engine, Conflict

class Transaction(BaseModel):
    model_config=ConfigDict(extra='forbid',allow_inf_nan=False)
    transaction_id:str=Field(min_length=1,max_length=80,pattern=r'^[A-Za-z0-9_-]+$')
    customer_id:str=Field(min_length=1,max_length=80,pattern=r'^[A-Za-z0-9_-]+$')
    timestamp:datetime
    amount:float=Field(gt=0,le=10000000)
    device_id:str=Field(min_length=1,max_length=80)
    country:str=Field(pattern=r'^[A-Z]{2}$')
    home_country:str=Field(pattern=r'^[A-Z]{2}$')
    @field_validator('timestamp')
    @classmethod
    def timezone_required(cls,v):
        if v.tzinfo is None:raise ValueError('Timezone required')
        return v
class Feedback(BaseModel):
    transaction_id:str
    is_fraud:Literal[0,1]
@asynccontextmanager
async def lifespan(app):
    app.state.engine=Engine(os.getenv('FRAUD_DB','data/live.db'))
    yield
app=FastAPI(title='Fraud Risk Demo',version='1.0.0',lifespan=lifespan)
@app.get('/health')
def health():return {'status':'ok','model_version':app.state.engine.artifact['version']}
@app.post('/score')
def score(tx:Transaction):
    try:return app.state.engine.score(tx.model_dump(mode='json'))
    except Conflict as e:raise HTTPException(409,str(e))
@app.get('/transactions')
def transactions():return app.state.engine.recent()
@app.post('/feedback')
def feedback(f:Feedback):
    try:app.state.engine.feedback(f.transaction_id,f.is_fraud)
    except KeyError:raise HTTPException(404,'Transaction not found')
    return {'saved':True}
