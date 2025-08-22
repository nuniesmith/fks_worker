# FKS Worker Service

Background task execution & scheduling (data refresh, training jobs, maintenance).

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install .[scheduler,queue]
python -m fks_worker.main
```

## Next Steps

- Integrate distributed task queue (Redis/RQ or Celery) (internal package renamed to avoid stdlib clash)
- Add metrics & tracing hooks
- Implement retry/backoff policies
