# Graph-Aware SupportOps Agent

A portfolio-ready customer-support automation prototype using **FastAPI, LangGraph, MiniLM, Qdrant, PostgreSQL, and n8n**.

It classifies support requests, retrieves policy evidence, checks synthetic order data, creates tickets when human review is needed, and returns an auditable execution trace. The graph/explainability component connects this engineering project to graph learning and Shapley-based analysis.

> This is an educational prototype with synthetic data. It is not production-ready and does not connect to a real store, CRM, or payment provider.

## Features
- FastAPI REST API and webhook endpoint
- LangGraph workflow with explicit state and nodes
- MiniLM embeddings + Qdrant policy retrieval
- PostgreSQL customers, orders, and tickets
- Controlled order lookup with customer ownership check
- Human escalation and ticket creation
- Structured execution trace and logging
- Shapley-style attribution for a transparent escalation score
- Docker Compose: API, PostgreSQL, Qdrant, n8n
- Unit tests and a small evaluation script

## Quick start
```bash
cp .env.example .env
docker compose up --build
docker compose exec api python scripts/seed.py
```
Open API docs at http://localhost:8000/docs, n8n at http://localhost:5678, and Qdrant at http://localhost:6333/dashboard.

Example:
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"customer_id":"CUST-1001","message":"My order ORD-5001 is late. Can you check it?"}'
```

The first run downloads `sentence-transformers/all-MiniLM-L6-v2`. For wiring/tests without downloading a model, set `USE_HASH_EMBEDDINGS=true`; this deterministic fallback is **not semantic retrieval**.

## Local development
Python 3.11 is recommended.
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python scripts/seed.py
uvicorn app.main:app --reload
```
PostgreSQL and Qdrant must be running. Run tests with `pytest -q`.

## API
`POST /api/v1/chat` accepts `customer_id` and `message`. The response contains `answer`, `intent`, `status`, optional `ticket_id`, `trace`, and `retrieved_sources`.

`POST /api/v1/webhooks/ticket-event` is a starter webhook for n8n. It requires the `X-Webhook-Secret` header.

## n8n
Import `n8n/support_ticket_notification.json`. It contains a webhook and event-normalization node. Add your own approved email/Slack/CRM notification node and credentials.

## Configuration
See `.env.example`. `.env` is ignored by Git. The initial response path is deterministic and grounded in retrieved text; the optional LLM settings are reserved for a future generation adapter and are not yet wired into the response path.

## Evaluation
```bash
python evaluation/run_evaluation.py
```
This tiny synthetic set is a smoke test, not evidence of production performance. Expand it with human-labelled examples before reporting quality claims.

## Why graph + Shapley?
The relational customer/order/ticket structure captures explicit relationships. The Shapley-style module attributes a deterministic escalation score to its input features. It does **not** explain hidden LLM reasoning.

## Production hardening
Add authentication, authorization, tenant isolation, PII controls, rate limiting, migrations, retries/timeouts, durable queues, monitoring, secret management, audit retention, and human approval for consequential actions. Never allow an LLM unrestricted SQL or arbitrary external actions.

## Layout
```text
app/       FastAPI, LangGraph, RAG, database, tools, explainability
data/      synthetic policy documents
evaluation/ small offline smoke test
n8n/       importable workflow
scripts/   seed script
tests/     unit tests
```
