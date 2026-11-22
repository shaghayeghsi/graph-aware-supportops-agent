from sqlalchemy.orm import Session
from app.database.repository import get_order, create_ticket
def lookup_order(db: Session, order_id: str, customer_id: str):
    order = get_order(db, order_id, customer_id)
    if not order: return None
    return {"order_id": order.id, "status": order.status, "product": order.product,
            "tracking_status": order.tracking_status}
def open_support_ticket(db: Session, customer_id: str, category: str, description: str):
    ticket = create_ticket(db, customer_id, category, description)
    return {"ticket_id": ticket.id, "status": ticket.status}
