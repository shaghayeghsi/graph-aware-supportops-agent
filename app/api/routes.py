import logging
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.api.schemas import ChatRequest, ChatResponse, TicketEvent
from app.database.session import get_db
from app.database.repository import get_customer
from app.rag.retrieval import PolicyRetriever
from app.agents.graph import build_support_graph
from app.core.config import settings
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1")
_retriever = None
def get_retriever():
    global _retriever
    if _retriever is None: _retriever = PolicyRetriever()
    return _retriever
@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    if not get_customer(db, request.customer_id):
        raise HTTPException(status_code=404, detail="Customer not found")
    result = build_support_graph(get_retriever(), db).invoke({
        "customer_id": request.customer_id, "message": request.message, "trace": []})
    return ChatResponse(answer=result["answer"], intent=result["intent"], status=result["status"],
        ticket_id=(result.get("ticket") or {}).get("ticket_id"), trace=result.get("trace", []),
        retrieved_sources=[d["source"] for d in result.get("retrieved_docs", [])])
@router.post("/webhooks/ticket-event")
def ticket_event(event: TicketEvent, x_webhook_secret: str | None = Header(default=None)):
    if x_webhook_secret != settings.webhook_secret:
        raise HTTPException(status_code=401, detail="Invalid webhook secret")
    logger.info("Received ticket event: %s", event.model_dump())
    return {"accepted": True, "ticket_id": event.ticket_id, "event": event.event}
