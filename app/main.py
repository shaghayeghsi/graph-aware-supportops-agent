from fastapi import FastAPI
from app.api.routes import router
from app.core.config import settings
from app.core.logging_config import configure_logging
configure_logging()
app = FastAPI(title=settings.app_name, version="0.1.0",
              description="Graph-aware RAG support agent prototype.")
app.include_router(router)
@app.get("/health")
def health(): return {"status": "ok", "service": settings.app_name}
