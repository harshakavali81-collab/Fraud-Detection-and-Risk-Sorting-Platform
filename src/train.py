import json, time, hashlib
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import average_precision_score, precision_score, recall_score, fbeta_score, confusion_matrix, PrecisionRecallDisplay
from src.features import features, FEATURES

def run():
    for d in ['reports','models']: Path(d).mkdir(exist_ok=True)
    df=pd.read_csv('data/transactions.csv').sort_values('timestamp').reset_index(drop=True)
    assert df.transaction_id.is_unique and df.amount.gt(0).all() and not df.isna().any().any()
    history={}; rows=[]
    for r in df.to_dict('records'):
        rows.append(features(r,history.get(r['customer_id'],[])))
        history.setdefault(r['customer_id'],[]).append(r)
    X=pd.DataFrame(rows)[FEATURES]; y=df.is_fraud
    a,b=int(len(df)*.6),int(len(df)*.8)
    models={'logistic':make_pipeline(StandardScaler(),LogisticRegression(max_iter=1000)),
            'random_forest':RandomForestClassifier(n_estimators=120,max_depth=8,min_samples_leaf=15,random_state=42,n_jobs=1)}
    comparison=[]
    for name,m in models.items():
        m.fit(X.iloc[:a],y.iloc[:a]); prob=m.predict_proba(X.iloc[a:b])[:,1]
        comparison.append({'model':name,'validation_average_precision':average_precision_score(y.iloc[a:b],prob)})
    winner=max(comparison,key=lambda r:r['validation_average_precision'])['model']; model=models[winner]
    val=model.predict_proba(X.iloc[a:b])[:,1]
    candidates=np.linspace(.005,.8,160)
    low=float(max(candidates,key=lambda t:fbeta_score(y.iloc[a:b],val>=t,beta=2,zero_division=0)))
    # Review threshold limits high-priority queue to approximately the highest-risk 5% on validation.
    high=float(max(low+.001,np.quantile(val,.95)))
    artifact={'model':model,'features':FEATURES,'verify_threshold':low,'review_threshold':high,'version':'synthetic-v1'}
    joblib.dump(artifact,'models/fraud_model.joblib',compress=3)
    start=time.perf_counter();prob=model.predict_proba(X.iloc[b:])[:,1]; elapsed=time.perf_counter()-start
    pred=prob>=low; tn,fp,fn,tp=confusion_matrix(y.iloc[b:],pred,labels=[0,1]).ravel()
    metrics=dict(selected_model=winner,train_rows=a,validation_rows=b-a,test_rows=len(df)-b,
        test_fraud_rate=float(y.iloc[b:].mean()),average_precision=float(average_precision_score(y.iloc[b:],prob)),
        precision=float(precision_score(y.iloc[b:],pred,zero_division=0)),recall=float(recall_score(y.iloc[b:],pred,zero_division=0)),
        false_positive_rate=float(fp/max(tn+fp,1)),alert_rate=float(pred.mean()),
        fraud_value_recall=float(df.iloc[b:].loc[(y.iloc[b:]==1)&pred,'amount'].sum()/df.iloc[b:].loc[y.iloc[b:]==1,'amount'].sum()),
        verify_threshold=low,review_threshold=high,tn=int(tn),fp=int(fp),fn=int(fn),tp=int(tp),
        batch_inference_ms_per_row=elapsed/len(prob)*1000,comparison=comparison,
        data_sha256=hashlib.sha256(Path('data/transactions.csv').read_bytes()).hexdigest())
    Path('reports/metrics.json').write_text(json.dumps(metrics,indent=2))
    out=df.iloc[b:].copy();out['risk_score']=np.round(prob*100,2)
    out['decision']=np.where(prob>=high,'review',np.where(prob>=low,'verify','approve'))
    out.to_csv('reports/test_predictions.csv',index=False)
    X.to_csv('data/features.csv',index=False)
    fig,ax=plt.subplots(figsize=(7,4));PrecisionRecallDisplay.from_predictions(y.iloc[b:],prob,ax=ax)
    ax.set_title('Synthetic holdout: precision and recall');fig.tight_layout();fig.savefig('reports/precision_recall.png',dpi=150);plt.close(fig)
    fig,ax=plt.subplots(figsize=(7,4));out.groupby('decision').size().reindex(['approve','verify','review'],fill_value=0).plot.bar(ax=ax,color=['#2d8b75','#c99b28','#c65353'])
    ax.set_title('Synthetic holdout: decisions');ax.set_ylabel('Transactions');ax.tick_params(axis='x',rotation=0)
    fig.tight_layout();fig.savefig('reports/decisions.png',dpi=150);plt.close(fig)
    print(json.dumps(metrics,indent=2))
if __name__=='__main__':run()
