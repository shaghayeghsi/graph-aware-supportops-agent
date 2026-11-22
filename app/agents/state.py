from typing import TypedDict
class SupportState(TypedDict, total=False):
    customer_id: str
    message: str
    intent: str
    order_id: str | None
    order_info: dict | None
    retrieved_docs: list[dict]
    escalation: dict
    ticket: dict | None
    answer: str
    status: str
    trace: list[dict]
