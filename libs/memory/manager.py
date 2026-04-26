import logging
from typing import Optional
from mem0 import Mem0
from .config import settings

logger = logging.getLogger(__name__)


class MemoryManager:
    def __init__(self):
        self.client = Mem0(
            backend=settings.backend,
            qdrant_url=settings.qdrant_url,
            collection_name=settings.qdrant_collection,
            embeddings_model=settings.ollama_model,
            embeddings_provider="ollama",
        )
        logger.info(f"MemoryManager initialized with backend={settings.backend}")

    def save(self, text: str, tags: Optional[list[str]] = None, source: str = "manual") -> dict:
        payload = {"text": text, "source": source}
        if tags:
            payload["tags"] = tags
        result = self.client.add(text, metadata=payload)
        logger.info(f"Saved memory: {result.get('id', 'unknown')}")
        return result

    def search(self, query: str, limit: int = 5) -> list[dict]:
        results = self.client.search(query, limit=limit)
        logger.info(f"Search '{query}': {len(results)} results")
        return results

    def get(self, memory_id: str) -> dict:
        return self.client.get(memory_id)

    def delete(self, memory_id: str) -> dict:
        result = self.client.delete(memory_id)
        logger.info(f"Deleted memory: {memory_id}")
        return result

    def list_recent(self, limit: int = 10) -> list[dict]:
        all_memories = self.client.get_all(limit=100)
        return all_memories[:limit]