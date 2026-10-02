"""Optional at-least-once Kafka bridge; requires an external broker."""
import argparse,json,urllib.request
import pandas as pd

def main():
    from kafka import KafkaProducer,KafkaConsumer
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['produce','consume']);p.add_argument('--bootstrap',default='localhost:9092');p.add_argument('--count',type=int,default=300);p.add_argument('--url',default='http://127.0.0.1:8000');a=p.parse_args()
    if a.mode=='produce':
        producer=KafkaProducer(bootstrap_servers=a.bootstrap,acks='all',value_serializer=lambda x:json.dumps(x).encode())
        for r in pd.read_csv('data/transactions.csv').head(a.count).drop(columns=['is_fraud']).to_dict('records'):
            producer.send('transactions',key=r['customer_id'].encode(),value=r).get(timeout=30)
        producer.flush();producer.close()
    else:
        consumer=KafkaConsumer('transactions',bootstrap_servers=a.bootstrap,group_id='fraud-demo',enable_auto_commit=False,auto_offset_reset='earliest',value_deserializer=lambda x:json.loads(x.decode()),max_poll_records=1)
        try:
            for msg in consumer:
                req=urllib.request.Request(a.url+'/score',data=json.dumps(msg.value).encode(),headers={'Content-Type':'application/json'})
                with urllib.request.urlopen(req,timeout=30) as response:print(response.read().decode())
                consumer.commit()
        finally:consumer.close()
if __name__=='__main__':main()
