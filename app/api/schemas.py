from pydantic import BaseModel, Field
class ChatRequest(BaseModel):
    customer_id: str = Field(min_length=1, max_length=40)
    message: str = Field(min_length=2, max_length=4000)
class ChatResponse(BaseModel):
    answer: str
    intent: str
    status: str
    ticket_id: str | None = None
    trace: list[dict]
    retrieved_sources: list[str]
class TicketEvent(BaseModel):
    ticket_id: str
    customer_id: str
    event: str = "ticket_created"
