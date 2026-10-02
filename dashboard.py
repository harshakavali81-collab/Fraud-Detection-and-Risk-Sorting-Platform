import json,os,uuid,urllib.request,urllib.error
from datetime import datetime,timezone
import pandas as pd
import streamlit as st
st.set_page_config(page_title='Fraud Risk Monitor',layout='wide')
st.title('Fraud Detection & Risk Scoring')
st.caption('Portfolio demo | Synthetic transactions | Scores are not calibrated fraud probabilities')
API=os.getenv('API_URL','http://127.0.0.1:8000')
def request(path,payload=None):
    req=urllib.request.Request(API+path,data=None if payload is None else json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(req,timeout=30) as r:return json.loads(r.read())
with st.sidebar.form('score'):
    st.subheader('Score a transaction')
    customer=st.text_input('Customer ID','C0001');device=st.text_input('Device ID','C0001-phone')
    amount=st.number_input('Amount (INR)',min_value=1.0,max_value=10000000.0,value=1500.0)
    country=st.selectbox('Transaction country',['IN','US','GB']);home=st.selectbox('Home country',['IN','US','GB'])
    submitted=st.form_submit_button('Score transaction')
if submitted:
    try:st.json(request('/score',dict(transaction_id='manual-'+uuid.uuid4().hex,customer_id=customer,timestamp=datetime.now(timezone.utc).isoformat(),amount=amount,device_id=device,country=country,home_country=home)))
    except Exception as e:st.error(str(e))
@st.fragment(run_every='3s')
def monitor():
    try:df=pd.DataFrame(request('/transactions'))
    except Exception as e:st.error('Start the API first: '+str(e));return
    st.subheader('Latest 200 transactions')
    if df.empty:st.info('Run the simulator or score a transaction in the sidebar.');return
    cols=st.columns(3);cols[0].metric('Visible transactions',len(df));cols[1].metric('Review queue',int((df.decision=='review').sum()));cols[2].metric('Mean risk score',f'{df.risk_score.mean():.1f}')
    left,right=st.columns(2)
    left.bar_chart(df.decision.value_counts());right.line_chart(df.sort_values('timestamp').set_index('timestamp').risk_score)
    st.dataframe(df,width='stretch',hide_index=True)
    st.download_button('Download visible transactions',df.to_csv(index=False),'transactions.csv')
monitor()
with st.expander('Record a review outcome'):
    with st.form('feedback'):
        tid=st.text_input('Transaction ID');label=st.selectbox('Confirmed fraud',[0,1])
        if st.form_submit_button('Save outcome'):
            try:st.success(request('/feedback',{'transaction_id':tid,'is_fraud':label}))
            except Exception as e:st.error(str(e))
