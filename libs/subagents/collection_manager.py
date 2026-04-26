"""
Collection Manager Subagent — Hermes Second Brain
Spawned by Hermes to manage Qdrant collections lifecycle.
"""

import logging
from typing import Optional
import requests

logger = logging.getLogger(__name__)


class CollectionManager:
    """
    Subagente responsável por gerenciar collections Qdrant.
    Criação, deleção, verificação de saúde.
    """

    QDRANT_URL = "http://localhost:6333"
    QDRANT_API_KEY: Optional[str] = None

    def __init__(self, name: str = "collection-manager"):
        self.name = name
        if not CollectionManager.QDRANT_API_KEY:
            from ..memory.config import settings
            CollectionManager.QDRANT_API_KEY = getattr(settings, 'qdrant_api_key', None)

        logger.info("CollectionManager initialized")

    def _headers(self) -> dict:
        return {
            "api-key": self.QDRANT_API_KEY or "",
            "Content-Type": "application/json"
        }

    def create_collection(self, name: str, vector_size: int = 768, distance: str = "Cosine") -> dict:
        """
        Cria uma nova collection no Qdrant.
        """
        payload = {
            "vectors": {
                "size": vector_size,
                "distance": distance
            }
        }

        try:
            resp = requests.put(
                f"{self.QDRANT_URL}/collections/{name}",
                json=payload,
                headers=self._headers(),
                timeout=10
            )
            resp.raise_for_status()
            logger.info(f"Created collection: {name}")
            return {"success": True, "collection": name}
        except Exception as e:
            logger.error(f"Failed to create collection {name}: {e}")
            return {"success": False, "error": str(e), "collection": name}

    def delete_collection(self, name: str) -> dict:
        """
        Deleta uma collection do Qdrant.
        """
        try:
            resp = requests.delete(
                f"{self.QDRANT_URL}/collections/{name}",
                headers=self._headers(),
                timeout=10
            )
            resp.raise_for_status()
            logger.info(f"Deleted collection: {name}")
            return {"success": True, "collection": name}
        except Exception as e:
            logger.error(f"Failed to delete collection {name}: {e}")
            return {"success": False, "error": str(e), "collection": name}

    def list_collections(self) -> list[str]:
        """
        Lista todas as collections.
        """
        try:
            resp = requests.get(
                f"{self.QDRANT_URL}/collections",
                headers=self._headers(),
                timeout=10
            )
            resp.raise_for_status()
            data = resp.json()
            return [c["name"] for c in data.get("result", {}).get("collections", [])]
        except Exception as e:
            logger.error(f"Failed to list collections: {e}")
            return []

    def collection_info(self, name: str) -> dict:
        """
        Retorna informações de uma collection.
        """
        try:
            resp = requests.get(
                f"{self.QDRANT_URL}/collections/{name}",
                headers=self._headers(),
                timeout=10
            )
            resp.raise_for_status()
            return resp.json().get("result", {})
        except Exception as e:
            logger.error(f"Failed to get info for {name}: {e}")
            return {"error": str(e)}

    def health_check(self) -> dict:
        """
        Verifica saúde do Qdrant.
        """
        try:
            resp = requests.get(
                f"{self.QDRANT_URL}/collections",
                headers=self._headers(),
                timeout=5
            )
            if resp.status_code == 200:
                collections = [c["name"] for c in resp.json().get("result", {}).get("collections", [])]
                return {
                    "status": "healthy",
                    "collections": len(collections),
                    "collection_names": collections
                }
            return {"status": "unhealthy", "code": resp.status_code}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}

    def stats(self) -> dict:
        """
        Retorna estatísticas de todas as collections.
        """
        collections = self.list_collections()
        stats = []

        for col_name in collections:
            info = self.collection_info(col_name)
            stats.append({
                "name": col_name,
                "vectors": info.get("vectors_count", 0),
                "status": info.get("status", "unknown")
            })

        return {
            "total_collections": len(collections),
            "collections": stats,
            "agent": self.name
        }
