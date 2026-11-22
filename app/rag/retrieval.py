import logging
from qdrant_client import QdrantClient, models
from app.core.config import settings
from app.rag.embeddings import Embedder
logger = logging.getLogger(__name__)
class PolicyRetriever:
    def __init__(self):
        self.embedder = Embedder()
        self.client = QdrantClient(url=settings.qdrant_url)
    def ensure_collection(self):
        names = {c.name for c in self.client.get_collections().collections}
        if settings.qdrant_collection not in names:
            self.client.create_collection(collection_name=settings.qdrant_collection,
                vectors_config=models.VectorParams(size=self.embedder.dimension, distance=models.Distance.COSINE))
    def index_documents(self, docs: list[dict]):
        self.ensure_collection()
        vectors = self.embedder.encode([d["text"] for d in docs])
        points = [models.PointStruct(id=i, vector=vectors[i],
                  payload={"text": d["text"], "source": d["source"]}) for i, d in enumerate(docs)]
        self.client.upsert(collection_name=settings.qdrant_collection, points=points)
    def search(self, query: str, limit: int = 3) -> list[dict]:
        try:
            self.ensure_collection()
            vector = self.embedder.encode([query])[0]
            hits = self.client.search(collection_name=settings.qdrant_collection, query_vector=vector, limit=limit)
            return [{"text": h.payload["text"], "source": h.payload["source"], "score": h.score} for h in hits]
        except Exception:
            logger.exception("Policy retrieval failed")
            return []
