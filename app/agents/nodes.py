import re
from sqlalchemy.orm import Session
from app.agents.state import SupportState
from app.database.repository import get_customer_tickets
from app.tools.business_tools import lookup_order, open_support_ticket
from app.explainability.shapley_explainer import explain_escalation
def _trace(state, event, **details):
    return state.get("trace", []) + [{"event": event, **details}]
def classify_node(state: SupportState) -> dict:
    msg = state["message"].lower()
    match = re.search(r"\bORD-[A-Z0-9-]+\b", state["message"], re.I)
    if any(x in msg for x in ["refund", "return", "مرجوع", "بازگشت"]): intent = "return_request"
    elif any(x in msg for x in ["late", "delivery", "where is", "نرسیده", "تاخیر", "سفارش"]): intent = "order_status"
    elif any(x in msg for x in ["broken", "damaged", "خراب", "شکسته"]): intent = "damaged_item"
    else: intent = "general_question"
    return {"intent": intent, "order_id": match.group(0).upper() if match else None,
            "trace": _trace(state, "intent_classified", intent=intent)}
def retrieve_node(state: SupportState, retriever):
    docs = retriever.search(state["message"], limit=3)
    return {"retrieved_docs": docs, "trace": _trace(state, "policy_retrieval",
            result_count=len(docs), sources=[d["source"] for d in docs])}
def business_node(state: SupportState, db: Session):
    info = lookup_order(db, state["order_id"], state["customer_id"]) if state.get("order_id") else None
    return {"order_info": info, "trace": _trace(state, "business_tool_executed",
            tool="lookup_order" if state.get("order_id") else "none", found=bool(info))}
def decision_node(state: SupportState, db: Session):
    prior = get_customer_tickets(db, state["customer_id"])
    repeat = 1.0 if prior else 0.0
    delayed = 1.0 if state.get("order_info") and any(
        x in state["order_info"]["tracking_status"].lower() for x in ["delayed", "exception", "تاخیر"]) else 0.0
    negative = 1.0 if any(x in state["message"].lower() for x in
        ["angry", "unacceptable", "terrible", "عصبانی", "افتضاح"]) else 0.0
    explanation = explain_escalation({"repeat_contact": repeat, "delivery_delay": delayed,
                                      "negative_sentiment": negative})
    ticket = None
    if explanation["escalate"] or state["intent"] in {"return_request", "damaged_item"}:
        ticket = open_support_ticket(db, state["customer_id"], state["intent"], state["message"])
    return {"escalation": explanation, "ticket": ticket,
            "status": "escalated" if ticket else "answered",
            "trace": _trace(state, "escalation_decision", escalated=bool(ticket), explanation=explanation)}
def respond_node(state: SupportState):
    if state.get("status") == "escalated":
        answer = f"Your request was forwarded to support. Reference: {state['ticket']['ticket_id']}."
    elif state.get("order_info"):
        o = state["order_info"]
        answer = f"Order {o['order_id']} is {o['status']}. Tracking: {o['tracking_status']}."
    elif state.get("retrieved_docs"):
        answer = "Relevant policy information: " + " ".join(d["text"] for d in state["retrieved_docs"][:2])[:700]
    else:
        answer = "I could not verify enough information. Please provide an order ID or request human support."
    return {"answer": answer, "trace": _trace(state, "response_generated", status=state.get("status"))}
