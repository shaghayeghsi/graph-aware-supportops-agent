# Architecture notes

1. FastAPI validates the request and checks the customer record.
2. LangGraph classifies intent and retrieves policy evidence from Qdrant.
3. A controlled order lookup checks that the order belongs to the requesting customer.
4. A transparent weighted score uses repeat contact, delivery delay, and negative sentiment.
5. Requests above threshold, return requests, and damaged-item reports create tickets.
6. The response includes an execution trace and retrieved source identifiers.

The current graph is represented through relational customer/order/ticket tables in PostgreSQL.
The Shapley-style attribution is exact for the additive escalation score only; it is not an
explanation of arbitrary LLM outputs. The n8n export is a starter webhook workflow requiring
the user to configure an outbound notification integration.
