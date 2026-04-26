from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    backend: str = "qdrant"
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "will"
    ollama_url: str = "http://localhost:11434"
    ollama_model: str = "nomic-ai/e5-mistral-7b-instruct"
    tasks_db_path: str = "/srv/data/librarian/tasks.db"

    class Config:
        env_prefix = "MEM0_"


settings = Settings()