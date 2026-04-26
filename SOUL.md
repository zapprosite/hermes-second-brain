# Hermes Second Brain — SOUL.md

**Classification:** INTERNAL | **Owner:** Platform Engineering
**Last Audit:** 2026-04-26 | **Version:** 1.0.0

---

## Identity

**Name:** Hermes Second Brain
**Type:** Mem0-backed knowledge management for autonomous agents
**Location:** `/srv/hermes-second-brain`
**Purpose:** Long-term memory persistence, semantic search, and task management for Nexus SRE agents

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Hermes Second Brain                  │
├──────────────┬──────────────┬──────────────────────────┤
│   Mem0 API   │   Qdrant     │   Ollama (local)         │
│   :8642     │   :6333      │   :11434                 │
├──────────────┴──────────────┴──────────────────────────┤
│  Collections: will | second-brain | mem0migrations    │
│  Models: qwen2.5:3b (text) | nomic-embed-text        │
└─────────────────────────────────────────────────────────┘
```

---

## Environment Variables (Canonical)

```bash
# ═─ Core ═─────────────────────────────────────────────────
MEM0_BACKEND=qdrant
MEM0_API_KEY=                    # From vault or .env
MEM0_API_URL=http://localhost:8642

# ═─ Qdrant ═───────────────────────────────────────────────
MEM0_QDRANT_URL=http://localhost:6333
MEM0_QDRANT_COLLECTION=will
QDRANT_API_KEY=71cae77676e2a5fd552d172caa1c3200

# ═─ Ollama (local Gen5 NVMe) ═────────────────────────────
MEM0_OLLAMA_URL=http://localhost:11434
MEM0_OLLAMA_MODEL=qwen2.5:3b

# ═─ Tasks DB ═────────────────────────────────────────────
MEM0_TASKS_DB_PATH=/srv/data/librarian/tasks.db
```

---

## Security

### ✅ SAFE Operations
- Read from Mem0 collections (semantic search)
- Write to `will` collection (personal memories)
- Query task database

### ❌ FORBIDDEN
- Do NOT log API keys or secrets
- Do NOT store credentials in code
- Do NOT expose Mem0 API port externally
- Do NOT use hardcoded API keys (use env vars)

### Secrets Management
```bash
# Retrieve secrets from Infisical
vault kv get -format=json secret/monorepo | jq -r '.data.data'

# Never hardcode — always source from .env
source /srv/monorepo/.env
```

---

## Collections

| Collection | Purpose | Retention |
|------------|---------|-----------|
| `will` | Personal memories and context | Indefinite |
| `second-brain` | Knowledge graph and docs | Indefinite |
| `mem0migrations` | Migration history | 30 days |

---

## Skills

### `/memory` — Mem0 Memory Operations

```bash
/memory save <text> [tag1 tag2]   # Save memory with optional tags
/memory query <question>           # Semantic search
/memory list                       # List recent memories
/memory get <id>                   # Retrieve specific memory
/memory delete <id>                # Delete a memory
```

### `/task` — Task Management

```bash
/task new <title>                  # Create pending task
/task list                         # List pending tasks
/task done <id>                   # Mark task complete
/task stats                       # Pending vs done stats
```

---

## Health Check

```bash
# Verify Mem0 connectivity
curl -s http://localhost:8642/health

# Verify Qdrant collections
curl -s -H "api-key: $QDRANT_API_KEY" http://localhost:6333/collections | jq '.result.collections[].name'

# Verify Ollama models loaded
curl -s http://localhost:11434/api/tags | jq '.models[].name'
```

---

## Incident Response

If Hermes is unavailable:
1. Check container: `docker ps | grep hermes`
2. Check logs: `docker logs hermes-second-brain --tail 50`
3. Restart if needed: `docker restart hermes-second-brain`
4. Verify: `curl -s http://localhost:8642/health`

---

## Audit Log

```bash
echo "$(date '+%Y-%m-%d %H:%M:%S') - Hermes SOUL.md audited" >> /srv/logs/audit.log
```

---

**Nexus Framework:** docs/NEXUS-SRE-GUIDE.md
**Main Monorepo:** /srv/monorepo
