from pathlib import Path
from app.database.models import Base, Customer, Order
from app.database.session import engine, SessionLocal
from app.rag.retrieval import PolicyRetriever
ROOT = Path(__file__).resolve().parents[1]
def main():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if not db.get(Customer, "CUST-1001"):
            db.add(Customer(id="CUST-1001", name="Alex Morgan", email="alex@example.test"))
        if not db.get(Customer, "CUST-1002"):
            db.add(Customer(id="CUST-1002", name="Sam Lee", email="sam@example.test"))
        if not db.get(Order, "ORD-5001"):
            db.add(Order(id="ORD-5001", customer_id="CUST-1001", status="processing",
                         product="Wireless Headphones", tracking_status="Delayed at regional hub"))
        if not db.get(Order, "ORD-5002"):
            db.add(Order(id="ORD-5002", customer_id="CUST-1002", status="shipped",
                         product="Laptop Stand", tracking_status="In transit"))
        db.commit()
    finally: db.close()
    docs = [{"source": p.name, "text": p.read_text(encoding="utf-8")}
            for p in (ROOT / "data/knowledge_base").glob("*.txt")]
    PolicyRetriever().index_documents(docs)
    print(f"Seeded database and indexed {len(docs)} policy documents.")
if __name__ == "__main__": main()
