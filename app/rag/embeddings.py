import hashlib
import numpy as np
from app.core.config import settings
class Embedder:
    def __init__(self):
        self.model = None
        if not settings.use_hash_embeddings:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(settings.embedding_model)
    @property
    def dimension(self): return 384
    def encode(self, texts: list[str]) -> list[list[float]]:
        if self.model is not None:
            return self.model.encode(texts, normalize_embeddings=True).astype("float32").tolist()
        # Deterministic development fallback only; not semantic embeddings.
        vectors = []
        for text in texts:
            vec = np.zeros(self.dimension, dtype=np.float32)
            for token in text.lower().split():
                idx = int(hashlib.sha256(token.encode()).hexdigest(), 16) % self.dimension
                vec[idx] += 1
            norm = np.linalg.norm(vec)
            vectors.append((vec / norm if norm else vec).tolist())
        return vectors
