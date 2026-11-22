from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    app_name: str = "Graph-Aware SupportOps Agent"
    log_level: str = "INFO"
    database_url: str = "postgresql+psycopg://supportops:supportops@localhost:5432/supportops"
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "support_policy"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    use_hash_embeddings: bool = False
    webhook_secret: str = "change-me"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
settings = Settings()
