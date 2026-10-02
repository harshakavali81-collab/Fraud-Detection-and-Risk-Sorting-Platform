import argparse,time,json,urllib.request
import pandas as pd
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--count',type=int,default=100);p.add_argument('--delay',type=float,default=.2);p.add_argument('--url',default='http://127.0.0.1:8000');a=p.parse_args()
    for row in pd.read_csv('data/transactions.csv').head(a.count).drop(columns=['is_fraud']).to_dict('records'):
        req=urllib.request.Request(a.url+'/score',data=json.dumps(row).encode(),headers={'Content-Type':'application/json'})
        with urllib.request.urlopen(req,timeout=30) as response:print(response.read().decode())
        time.sleep(max(a.delay,0))
