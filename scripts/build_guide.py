from pathlib import Path
import json,html
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Image,Table,TableStyle,Preformatted
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
p=Path(__file__).resolve().parents[1];m=json.loads((p/'reports/metrics.json').read_text())
# Exportable architecture diagram with offline and online branches.
fig,ax=plt.subplots(figsize=(10,6));ax.set_xlim(0,10);ax.set_ylim(0,7);ax.axis('off')
nodes={'data':(1.5,6,'Historical data\nSynthetic labels'),'train':(5,6,'Shared features\nTrain + validation'),'model':(8.5,6,'Model artifact\nSchema + thresholds'),'events':(1.5,3.7,'Transaction source\nHTTP / optional Kafka'),'api':(5,3.7,'FastAPI\nValidate + score'),'db':(8.5,3.7,'SQLite\nHistory + decisions'),'dash':(5,1.3,'Streamlit\nQueue + feedback'),'analyst':(8.5,1.3,'Analyst outcomes\nConfirmed labels')}
for k,(x,y,t) in nodes.items():
 ax.add_patch(FancyBboxPatch((x-1.3,y-.45),2.6,.9,boxstyle='round,pad=.12',facecolor='#eaf1f7',edgecolor='#244864',linewidth=1.3));ax.text(x,y,t,ha='center',va='center',fontsize=10,color='#17324d')
for a,b in [('data','train'),('train','model'),('events','api'),('model','api'),('api','db'),('api','dash'),('dash','analyst'),('analyst','db')]:
 x,y,_=nodes[a];u,v,_=nodes[b];dx,dy=u-x,v-y
 if abs(dx)>abs(dy):x+=1.44*(1 if dx>0 else -1);u-=1.44*(1 if dx>0 else -1)
 else:y+=.6*(1 if dy>0 else -1);v-=.6*(1 if dy>0 else -1)
 ax.annotate('',xy=(u,v),xytext=(x,y),arrowprops={'arrowstyle':'->','color':'#39718e','lw':1.5})
fig.tight_layout();fig.savefig(p/'docs/architecture.png',dpi=170,bbox_inches='tight');plt.close(fig)
chapters=[
('1. Purpose, scope and deliverables',[
'This project demonstrates a real-time fraud-risk workflow for a portfolio. Incoming transactions receive a numeric risk score and an approve, verify or review decision. The decisions are simulated; the application does not execute payments, send OTPs or block accounts.',
'The working local path uses Python, Pandas, scikit-learn, FastAPI, SQLite and Streamlit. SQLite removes the need to configure a database server for the first demonstration. The optional Kafka bridge can connect an existing broker to the same API.',
'Included: 12,000 synthetic transactions, shared feature code, trained model, validation and holdout reports, API, dashboard, simulator, SQL, notebook, automated tests, Docker configuration, Excel workbook, diagrams and interview notes.',
'All events, customers and fraud labels are synthetic. Results explain this artificial dataset only. The project is a complete local portfolio demonstration; production deployment and a live Kafka broker remain separate operational work.'
]),
('2. Architecture and complete workflow',[
'Data flows through two paths. Offline training generates transactions, validates them, computes features in time order, trains candidates and evaluates a reserved holdout. Online scoring uses the same feature function, retrieves prior customer events from SQLite, loads the saved model and thresholds, then persists a decision.',
'The dashboard calls the API. It shows the latest 200 events and refreshes every three seconds. Its counts are explicitly scoped to these visible events. The analyst can record a confirmed outcome, which is stored separately from the original risk decision.',
'Workflow: define request and fraud outcome; generate data; validate; explore; calculate historical features; split by time; train; choose thresholds; evaluate; start API; replay transactions; review dashboard; collect outcomes; monitor shifts; retrain offline.'
]),
('3. Data and feature engineering',[
'Each transaction contains transaction_id, customer_id, timestamp, amount, device_id, country and home_country. Timestamps must include a timezone and are normalized to UTC. Amounts are INR and must be positive. is_fraud appears only in historical labeled data and is rejected as an extra API input.',
'The generator uses seed 42 and 30-second event spacing. Customers, amounts, device changes and foreign-country events are sampled. Fraud labels are Bernoulli samples from a declared artificial risk function, not real chargeback data. This limits generalization and deliberately avoids a perfectly separable label.',
'Features: log(1+amount); amount divided by the preceding 24-hour mean; number of customer events in the preceding hour; unseen device indicator relative to earlier customer devices; UTC hour before 06:00; country differing from home country.',
'Only strictly earlier events are eligible for history. The current event is appended after feature calculation. For no recent history, the amount ratio is one. A first-ever device is not called new until earlier customer history exists. UTC night is a teaching simplification, not the customer local timezone.',
'Input validation checks positive amounts, finite values, identifier length, country-code shape and timezone presence. This is format validation, not full ISO-country membership or account-ownership verification.'
]),
('4. Modeling and evaluation',[
'The earliest 7,200 rows train the models. The next 2,400 choose the model and thresholds. The final 2,400 are the holdout. Earlier event history can cross split boundaries because it would have existed at scoring time; fraud labels never become historical features.',
'Candidates are Logistic Regression with training-only standardization and Random Forest with bounded depth and leaf size. The highest validation average precision wins. No oversampling is applied. The chosen model is Random Forest.',
'The verify threshold maximizes validation F2 over a fixed grid. F2 gives recall more emphasis than precision. The review threshold uses the larger of the validation 95th percentile and verify threshold plus 0.001. It targets an approximate high-priority queue size, not a guaranteed future service level.',
'On the synthetic holdout, average precision is 0.1807, precision is 5.59%, recall is 53.33%, false-positive rate is 11.39%, and alert rate is 11.92%. There are 16 true positives, 270 false positives, 14 false negatives and 2,100 true negatives.',
'The result demonstrates a trade-off: 286 events are flagged to capture 16 of 30 fraud events. The false-alert burden is substantial. Captured fraud amount is 86.49% of labeled fraud amount; this is not money saved. Human intervention cost and real loss avoidance are not measured.'
]),
('5. Risk decisions, persistence and API',[
'Score equals 100 times the model output. At this trained version, verify begins at model output 0.025 and review at about 0.05734. Scores are rounded only for display; decisions use the unrounded output. A score is not a calibrated fraud probability and a high score does not prove fraud.',
'GET /health reports service and model status. POST /score accepts a transaction. GET /transactions returns the latest 200 stored events. POST /feedback records a binary confirmed outcome for an existing transaction. Interactive schemas are available at /docs when the API is running.',
'An atomic SQLite transaction covers history read and decision insert. transaction_id is a primary key. An identical retry returns the original result. A reused ID with a changed payload returns HTTP 409. Strictly non-increasing event times for one customer also return 409.',
'Reason flags indicate observed conditions such as a new device or elevated amount. They are not SHAP values or causal explanations. Feedback accepts 0 or 1 and uses a foreign key. Unreviewed events are not assumed legitimate.',
'Only one small local writer workload is intended. SQLite locks serialize writes and full customer-history scans grow with usage. A larger system needs bounded feature storage, consistent device state, managed schema migrations and load-tested concurrency.'
]),
('6. VS Code setup and demonstration',[
'Install Python 3.12 and extract the ZIP. Open fraud-platform in VS Code. In its terminal run python -m venv .venv. Activate with .venv\\Scripts\\Activate.ps1 on Windows PowerShell or source .venv/bin/activate on macOS/Linux. If PowerShell blocks activation, use .venv\\Scripts\\python.exe directly rather than changing machine policy.',
'Run python -m pip install -r requirements.txt. Run python -m src.train to regenerate a model compatible with your installed libraries. Run python -m pytest -q. Then start python -m uvicorn src.api:app --host 127.0.0.1 --port 8000.',
'In a second activated terminal run python -m streamlit run dashboard.py and open http://localhost:8501. In a third activated terminal run python -m src.simulate --count 300 --delay 0.1. Observe scores and the review queue, then enter a transaction manually.',
'Use the API documentation at http://localhost:8000/docs to replay an ID and inspect validation errors. Record an outcome through the dashboard. SQLite state lives in data/live.db by default.',
'Replay begins at historical time. If a customer already has a current-time manual event, older replay events for that customer are rejected. Use a new FRAUD_DB path for a clean demonstration. Retraining changes the saved artifact; restart the API to load it.'
]),
('7. Tests, monitoring and deployment boundaries',[
'Automated tests cover scoring, idempotent retries, conflicting payloads, out-of-order transactions, invalid amounts, naive timestamps, malformed country codes, unknown fields, feedback existence, binary outcomes and future-event exclusion. See reports/test_results.txt for the actual run.',
'The live check launches the API, replays 300 transactions and executes the Streamlit application using its test harness. reports/live_check.json records results and local scoring timings. These timings exclude the final database insert/commit and network round trip; they are not production latency claims.',
'src/monitor.py compares training and holdout feature means and reports absolute standardized shifts. It is a descriptive batch check. It does not implement automated alerts, PSI thresholds or drift-triggered retraining. Monitor delayed-label precision, recall, queue capacity, errors, latency and feature distributions in a future operational system.',
'Dockerfile and compose.yaml provide local deployment configuration and persistent storage. Docker execution is not validated here. Kafka adapter code is supplied; the external broker path is not integration-tested here. Public hosting is not included.',
'Before production use, add authentication and authorization, encrypted transport, rate limits, secrets handling, real-time feature consistency, monitoring, backups, calibration, cost-aware policies and validation on approved real data. This demo binds to local interfaces and contains no real personal data.'
]),
('8. Project structure, GitHub and interview use',[
'src/ owns generation, features, training, API, scoring, simulation and optional transport. sql/ contains the schema and queries. tests/ validates behavior. models/ contains the trusted demonstration artifact. data/ contains synthetic source and derived features. notebooks/ contains EDA. reports/ contains metrics and Excel. docs/ contains this guide, model card and diagrams.',
'Open reports/Fraud_Analytics.xlsx for a formula-linked holdout summary, predictions and dictionary. Counts and ratios are derived from included predictions. The workbook is an analysis snapshot, not connected to the live API. Run the EDA notebook to explore data and consult source scripts for exact implementation.',
'The repository includes a GitHub Actions workflow to install dependencies, train and run tests. A pushed workflow is configuration, not evidence of a completed remote CI run. Review Actions after GitHub upload.',
'In interviews, explain the problem, architecture, chronological split, duplicate handling, cold start, threshold trade-off and synthetic-data limitations. Do not claim prevented losses, real banking deployment or production throughput. Use docs/INTERVIEW.md for a five-minute demo and resume bullets.',
'Reproduction: python -m src.generate; python -m src.train; python -m src.monitor; python -m pytest -q. README.md includes startup instructions. The PDF and Excel are delivered snapshots; rerunning training refreshes machine-readable reports and plots, while authored documentation must be updated to match new results.'
])]
(p/'docs/PROJECT_GUIDE.md').write_text('# Real-Time Fraud Detection and Risk Scoring Platform\n\n'+'\n\n'.join('## '+title+'\n\n'+'\n\n'.join(pars) for title,pars in chapters))
styles=getSampleStyleSheet();styles.add(ParagraphStyle(name='BodyGuide',fontName='Helvetica',fontSize=10.5,leading=16,spaceAfter=12,textColor=colors.HexColor('#263b4e')))
styles['Heading1'].textColor=colors.HexColor('#17324D');styles['Heading1'].fontSize=21;styles['Heading1'].leading=26;styles['Heading1'].spaceAfter=20
story=[]
for idx,(title,pars) in enumerate(chapters):
 if idx:story.append(PageBreak())
 story.append(Paragraph(title,styles['Heading1']))
 if idx==0:
  story.append(Paragraph('Real-Time Fraud Detection and Risk Scoring Platform',styles['Title']));story.append(Paragraph('Portfolio project guide | Kavali Harshavardhan',styles['BodyGuide']));story.append(Spacer(1,15))
 for para in pars:story.append(Paragraph(html.escape(para),styles['BodyGuide']))
 if idx==1:story.append(Image(str(p/'docs/architecture.png'),width=470,height=282))
 if idx==3:story.append(Image(str(p/'reports/precision_recall.png'),width=420,height=240))
def footer(c,doc):
 c.setStrokeColor(colors.HexColor('#ccd8e1'));c.line(48,40,547,40);c.setFont('Helvetica',8);c.setFillColor(colors.HexColor('#526777'));c.drawString(48,27,'Fraud-risk portfolio demo | Synthetic data');c.drawRightString(547,27,str(doc.page))
SimpleDocTemplate(str(p/'docs/Fraud_Platform_Guide.pdf'),pagesize=(595,842),rightMargin=48,leftMargin=48,topMargin=45,bottomMargin=55).build(story,onFirstPage=footer,onLaterPages=footer)
print('Guide and architecture generated')
