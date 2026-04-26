# Hermes Second Brain — SOUL.md

**Classification:** INTERNAL | **Owner:** Platform Engineering
**Last Audit:** 2026-04-26 | **Version:** 1.1.0

---

## Identity

**Name:** Hermes Second Brain
**Type:** Mem0-backed knowledge management for autonomous agents
**Location:** `/srv/hermes-second-brain`
**Purpose:** Long-term memory persistence, semantic search, and task management for Nexus SRE agents
**API Rate Limit:** 500 RPM (MiniMax M2.7 plano)

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                      Hermes Second Brain                              │
├──────────────┬──────────────┬──────────────────────────────────────┤
│   Mem0 API   │   Qdrant     │   Ollama (Gen5 NVMe)                   │
│   :8642      │   :6333      │   :11434                              │
├──────────────┴──────────────┴──────────────────────────────────────┤
│  Collections: will | second-brain | mem0migrations | + 4 instances  │
│  Models: qwen2.5:3b (text) | nomic-embed-text | qwen2.5vl:3b (VL)   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Environment Variables (Canonical)

```bash
# ═─ Core ═─────────────────────────────────────────────────
source /srv/monorepo/.env

MEM0_BACKEND=qdrant
MEM0_API_KEY=
MEM0_API_URL=http://localhost:8642

# ═─ Qdrant (Gen5 NVMe /tank/qdrant) ═─────────────────────
MEM0_QDRANT_URL=http://localhost:6333
MEM0_QDRANT_COLLECTION=will
QDRANT_API_KEY=71cae77676e2a5fd552d172caa1c3200

# ═─ Ollama (Gen5 NVMe /tank/models) ═────────────────────
MEM0_OLLAMA_URL=http://localhost:11434
MEM0_OLLAMA_MODEL=qwen2.5:3b

# ═─ Tasks DB (Gen3 NVMe /srv/data/librarian) ═───────────
MEM0_TASKS_DB_PATH=/srv/data/librarian/tasks.db

# ═─ MiniMax M2.7 (500 RPM rate limit) ═─────────────────
MINIMAX_API_KEY=sk-cp-etXmVd5gY30jOBe2a6AvTzWT4olPvnVBld7qcdWBdJqcSFSj4BSWt5YXXwXWkzNfixm8ZVVNxfmP12yC6S8IZhFR9YOlJDggNc6Wlbt0SY4-4jqBrHWG0rc
MINIMAX_API_BASE=https://api.minimax.io
```

---

## Security

### ✅ SAFE Operations
- Read from Mem0 collections (semantic search)
- Write to `will` collection (personal memories)
- Query task database
- Create/list collections via CollectionManager subagent

### ❌ FORBIDDEN
- Do NOT log API keys or secrets
- Do NOT store credentials in code
- Do NOT expose Mem0 API port externally
- Do NOT use hardcoded API keys (use env vars)
- Do NOT delete collections without Archivist backup

---

## Collections (Qdrant — Gen5 NVMe)

| Collection | Purpose | Instance | Status |
|------------|---------|----------|--------|
| `will` | Personal memories and context | Hermes | ✅ |
| `second-brain` | Knowledge graph and docs | Hermes | ✅ |
| `mem0migrations` | Migration history | Hermes | ✅ |
| `claude-code-memory` | Claude CLI memories | Claude Code | ✅ |
| `cursor-projects` | Cursor IDE projects | Cursor | ✅ |
| `vscode-memory` | VS Code Copilot | VS Code | ✅ |
| `codex-repo` | Codex CLI repos | Codex | ✅ |

**Storage:** `/tank/qdrant/` (Gen5 NVMe — Crucial T700 4TB)

---

## Subagents

Hermes spawns subagents as Python processes for specific operations:

### MemoryArchivist
**Path:** `libs/subagents/memory_archivist.py`
**Purpose:** Archive, compact, and tag memories

```python
from libs.subagents import MemoryArchivist

archivist = MemoryArchivist(collection="will")
archivist.archive_old_memories(days=30)
archivist.compact_memories(max_per_user=100)
archivist.tag_memories(query="projeto", add_tags=["important"])
archivist.stats()
```

### CollectionManager
**Path:** `libs/subagents/collection_manager.py`
**Purpose:** Qdrant collection lifecycle management

```python
from libs.subagents import CollectionManager

cm = CollectionManager()
cm.create_collection("new-instance", vector_size=768)
cm.delete_collection("old-instance")
cm.list_collections()
cm.health_check()
cm.stats()
```

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

# Verify Qdrant collections (7 total)
curl -s -H "api-key: $QDRANT_API_KEY" http://localhost:6333/collections | jq '.result.collections[].name'

# Verify Ollama models loaded (3 models)
curl -s http://localhost:11434/api/tags | jq '.models[].name'

# Verify Qdrant health
curl -s -H "api-key: $QDRANT_API_KEY" http://localhost:6333/collections | jq '.result'
```

---

## Storage Topology

```
 GEN5 NVMe (/tank - Crucial T700 4TB) — Performance crítica
 ┌─────────────────────────────────────────────────────────────────┐
 │  /tank/qdrant/               ← 7 collections Qdrant             │
 │  /tank/models/               ← Ollama blobs (5.1GB)           │
 │  /tank/docker-data/          ← Container persistent data        │
 └─────────────────────────────────────────────────────────────────┘

 GEN3 NVMe (/dev/nvme1n1 - Kingston SNV3S 1TB)
 ┌─────────────────────────────────────────────────────────────────┐
 │  / (root)                ← OS + Coolify                         │
 │  /home                   ← User home + configs                  │
 │  /srv/data/librarian/     ← SQLite tasks                        │
 │  /srv/data/redis/         ← Redis (sessions, cache, pub/sub)   │
 │  /srv/backups/            ← Backups                             │
 └─────────────────────────────────────────────────────────────────┘
```

---

## Incident Response

If Hermes is unavailable:
1. Check container: `docker ps | grep hermes`
2. Check logs: `docker logs hermes-second-brain --tail 50`
3. Restart if needed: `docker restart hermes-second-brain`
4. Verify: `curl -s http://localhost:8642/health`

If Qdrant is slow:
1. Check Gen5 NVMe: `zpool status tank`
2. Check I/O: `iostat -x 5`
3. Verify collections: `curl -s -H "api-key: $QDRANT_API_KEY" http://localhost:6333/collections`

---

## Audit Log

```bash
echo "$(date '+%Y-%m-%d %H:%M:%S') - Hermes SOUL.md audited" >> /srv/logs/audit.log
```

---

**Nexus Framework:** /srv/monorepo/docs/NEXUS-SRE-GUIDE.md
**Main Monorepo:** /srv/monorepo
**Version History:** git log --oneline
