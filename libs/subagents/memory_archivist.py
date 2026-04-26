"""
Memory Archivist Subagent — Hermes Second Brain
Spawned by Hermes to organize and archive memories across collections.
"""

import logging
import time
from typing import Optional
from ..memory.manager import MemoryManager

logger = logging.getLogger(__name__)


class MemoryArchivist:
    """
    Subagente responsável por arquivar e organizar memories.
    Cada instância pode operar em uma collection diferente.
    """

    def __init__(self, collection: str = "will", name: str = "memory-archivist"):
        self.name = name
        self.collection = collection
        self.memory = MemoryManager()
        self.memory.client.collection_name = collection
        logger.info(f"MemoryArchivist initialized for collection={collection}")

    def archive_old_memories(self, days: int = 30, tags: Optional[list[str]] = None) -> dict:
        """
        Arquiva memories mais antigas que 'days'.
        """
        cutoff = time.time() - (days * 86400)
        archived = 0

        all_memories = self.memory.client.get_all(limit=1000)
        for mem in all_memories:
            created = mem.get("created_at_timestamp", 0)
            if created < cutoff:
                tags = tags or []
                tags.append("archived")
                self.memory.client.update(mem["id"], metadata={"tags": tags})
                archived += 1

        logger.info(f"Archived {archived} memories older than {days} days")
        return {"archived": archived, "collection": self.collection}

    def compact_memories(self, max_per_user: int = 100) -> dict:
        """
        Compacta memories consolidando similares.
        Mantém apenas as 'max_per_user' mais recentes por source.
        """
        all_memories = self.memory.client.get_all(limit=1000)
        by_source = {}

        for mem in all_memories:
            source = mem.get("metadata", {}).get("source", "unknown")
            if source not in by_source:
                by_source[source] = []
            by_source[source].append(mem)

        deleted = 0
        for source, memories in by_source.items():
            if len(memories) > max_per_user:
                to_delete = memories[max_per_user:]
                for mem in to_delete:
                    self.memory.client.delete(mem["id"])
                    deleted += 1

        logger.info(f"Compacted {deleted} memories")
        return {"deleted": deleted, "collection": self.collection}

    def tag_memories(self, query: str, add_tags: list[str]) -> dict:
        """
        Adiciona tags a memories que matcham query.
        """
        results = self.memory.search(query, limit=100)
        tagged = 0

        for mem in results:
            current_tags = mem.get("metadata", {}).get("tags", [])
            new_tags = list(set(current_tags + add_tags))
            self.memory.client.update(mem["id"], metadata={"tags": new_tags})
            tagged += 1

        logger.info(f"Tagged {tagged} memories with {add_tags}")
        return {"tagged": tagged, "query": query, "tags": add_tags}

    def stats(self) -> dict:
        """
        Retorna estatísticas da collection.
        """
        all_memories = self.memory.client.get_all(limit=10000)
        return {
            "collection": self.collection,
            "total_memories": len(all_memories),
            "agent": self.name
        }
