from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from libs.memory import MemoryManager

router = APIRouter()
mm = MemoryManager()


class MemoryInput(BaseModel):
    text: str
    tags: Optional[list[str]] = None
    source: str = "manual"


class MemoryQuery(BaseModel):
    query: str
    limit: int = 5


@router.post("/")
def save_memory(input: MemoryInput):
    result = mm.save(input.text, input.tags, input.source)
    return {"success": True, "memory": result}


@router.post("/query")
def search_memory(input: MemoryQuery):
    results = mm.search(input.query, input.limit)
    return {"results": results}


@router.get("/{memory_id}")
def get_memory(memory_id: str):
    try:
        result = mm.get(memory_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{memory_id}")
def delete_memory(memory_id: str):
    try:
        result = mm.delete(memory_id)
        return {"success": True, "deleted": memory_id}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/")
def list_recent():
    memories = mm.list_recent(limit=10)
    return {"memories": memories}