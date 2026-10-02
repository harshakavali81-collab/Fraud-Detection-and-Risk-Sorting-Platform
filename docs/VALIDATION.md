# Validation record

11 passed, 1 warning in 2.34s

Warning: FastAPI TestClient uses the deprecated httpx interface in the installed Starlette version. Tests completed successfully.

## Live check

```json
{
  "events_scored": 300,
  "dashboard_metrics": 3,
  "dashboard_exceptions": 0,
  "scoring_ms_p50": 9.791,
  "scoring_ms_p95": 13.0251,
  "latency_scope": "Scoring measured inside engine, excluding final insert/commit and network. Single-process local demo."
}
```

Excel formulas were recalculated, summary counts reconciled to predictions, and all three sheets rendered. The 8-page PDF was rendered and visually checked. Kafka broker integration, Docker execution and remote GitHub Actions are not verified.
