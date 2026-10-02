import math
from datetime import datetime, timezone
FEATURES = ['log_amount', 'amount_ratio', 'count_1h', 'new_device', 'night', 'foreign']
def timestamp(value):
    t = datetime.fromisoformat(str(value).replace('Z', '+00:00'))
    if t.tzinfo is None:
        raise ValueError('Timestamp must include a timezone')
    return t.astimezone(timezone.utc)
def features(tx, history):
    now = timestamp(tx['timestamp'])
    prior = [r for r in history if timestamp(r['timestamp']) < now]
    recent = [r for r in prior if (now-timestamp(r['timestamp'])).total_seconds() <= 86400]
    avg = sum(r['amount'] for r in recent)/len(recent) if recent else tx['amount']
    return dict(zip(FEATURES, [math.log1p(tx['amount']), tx['amount']/max(avg,1),
        sum((now-timestamp(r['timestamp'])).total_seconds() <= 3600 for r in prior),
        int(bool(prior) and tx['device_id'] not in {r['device_id'] for r in prior}),
        int(now.hour < 6), int(tx['country'] != tx['home_country'])]))
