# Optional Kafka transport

Install `python -m pip install -r requirements-kafka.txt` and use an existing broker with a `transactions` topic. Broker setup, TLS and authentication depend on your deployment and are not bundled.

```bash
python -m src.kafka_bridge produce --bootstrap localhost:9092 --count 300
python -m src.kafka_bridge consume --bootstrap localhost:9092
```

Start the API first. Producer keys events by customer ID for per-customer partition ordering. Consumer disables auto-commit and commits after a successful HTTP response. A crash between HTTP response and offset commit causes replay; the API's idempotency handles it. Delivery is at-least-once, not globally exactly-once. Invalid/late events stop the consumer without committing; production needs an explicit dead-letter queue and operator decision. Use one consumer per demo group unless you validate rebalance behavior. The adapter is included but broker integration is not tested in this environment.
