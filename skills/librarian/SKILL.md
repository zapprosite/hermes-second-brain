# Librarian Skill — Hermes Second Brain

**Skill Version:** 1.1.0 | **Updated:** 2026-04-26
**Framework:** Mem0 + Qdrant + Ollama (qwen2.5:3b)

## Trigger
`/memory` or `/task` commands in Hermes Agent

## Environment

```bash
# ═─ Required env vars (from /srv/monorepo/.env) ═────────────
source /srv/monorepo/.env

MEM0_BACKEND=qdrant
MEM0_QDRANT_URL=http://localhost:6333
MEM0_QDRANT_COLLECTION=will
QDRANT_API_KEY=$QDRANT_API_KEY
MEM0_OLLAMA_URL=http://localhost:11434
MEM0_OLLAMA_MODEL=qwen2.5:3b
MEM0_TASKS_DB_PATH=/srv/data/librarian/tasks.db
```

## When to Use
When Hermes needs to persist context, save important decisions, or manage tasks across sessions.

## Commands

### /memory save
Save a memory to Mem0 → Qdrant
```
/memory save <text> [tag1 tag2]
```

### /memory query
Semantic search in memory
```
/memory query <question>
```

### /memory list
List recent memories

### /memory get <id>
Retrieve specific memory

### /memory delete <id>
Delete a memory

### /task new <title>
Create new task (pending)

### /task list
List pending tasks

### /task done <id>
Mark task done

### /task stats
Show pending vs done

## Health Check

```bash
# Verify Qdrant connectivity
curl -s -H "api-key: $QDRANT_API_KEY" http://localhost:6333/collections | jq '.result.collections[].name'

# Verify Ollama
curl -s http://localhost:11434/api/tags | jq '.models[].name'
```

## Setup
```bash
pip install -e /srv/hermes-second-brain
```

## SOUL.md
See `/srv/hermes-second-brain/SOUL.md` for full security and architecture documentation.
