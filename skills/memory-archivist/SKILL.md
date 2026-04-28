# Memory Archivist

## Name
Memory Archivist

## Purpose
Archive, compact, and tag memories in Qdrant collections.

## When to Use
After Execute phase, before Complete phase.

## Operations

### archive_session
Archive a completed session to long-term storage.
- **Parameters:** `collection`, `session_id`
- **Usage:** `libs/subagents/memory_archivist.py archive_session <collection> <session_id>`

### compact_memories
Compact overlapping memories into optimized representations.
- **Parameters:** `collection`, `batch_size`
- **Usage:** `libs/subagents/memory_archivist.py compact_memories <collection> <batch_size>`

### tag_memories
Apply tags to memories for improved retrieval.
- **Parameters:** `collection`, `tags`
- **Usage:** `libs/subagents/memory_archivist.py tag_memories <collection> <tags>`

## Usage
Invoke via subprocess call to `libs/subagents/memory_archivist.py`.

## Environment Variables
- `QDRANT_API_KEY` — Qdrant API key for vector database access
- `MEM0_API_KEY` — Mem0 API key for memory management
