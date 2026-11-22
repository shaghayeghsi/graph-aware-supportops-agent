from uuid import uuid4
from sqlalchemy.orm import Session
from app.database.models import Customer, Order, Ticket
def get_customer(db: Session, customer_id: str): return db.get(Customer, customer_id)
def get_order(db: Session, order_id: str, customer_id: str | None = None):
    order = db.get(Order, order_id)
    if order and customer_id and order.customer_id != customer_id: return None
    return order
def get_customer_tickets(db: Session, customer_id: str):
    return db.query(Ticket).filter(Ticket.customer_id == customer_id).all()
def create_ticket(db: Session, customer_id: str, category: str, description: str):
    item = Ticket(id=f"TKT-{uuid4().hex[:8].upper()}", customer_id=customer_id,
                  category=category, description=description, status="open")
    db.add(item); db.commit(); db.refresh(item); return item
