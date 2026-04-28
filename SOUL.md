# Hermes Second Brain — SOUL.md

> **⚠️ Security & Architecture Authority**
> **Classification:** INTERNAL | **Owner:** Platform Engineering
> **Version:** 2.0.0 | **Updated:** 2026-04-26

---

## Identity

| Attribute | Value |
|-----------|-------|
| **Name** | Hermes Second Brain |
| **Type** | Mem0-backed knowledge management |
| **Location** | `/srv/hermes-second-brain` |
| **Purpose** | Long-term memory for Nexus agents |
| **Rate Limit** | 500 RPM (MiniMax M2.7) |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         INTERNET                                      │
│                            │                                          │
│                            ▼                                          │
│                 ┌─────────────────────┐                              │
│                 │  Cloudflare Tunnel  │                              │
│                 │  *.zappro.site      │                              │
│                 └─────────────────────┘                              │
│                            │                                          │
│                            ▼                                          │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │              HERMES SECOND BRAIN                             │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────────────────┐ │   │
│  │  │ Mem0 API  │  │  Qdrant    │  │ Ollama                 │ │   │
│  │  │ :8642     │  │  :6333     │  │ :11434                 │ │   │
│  │  │ MiniMax   │  │  7 cols    │  │ qwen2.5:3b             │ │   │
│  │  │ M2.7      │  │  Gen5 NVMe │  │ nomic-embed-text       │ │   │
│  │  └────────────┘  └────────────┘  └────────────────────────┘ │   │
│  └──────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Environment Variables (Canonical)

```bash
# ══ Core ════════════════════════════════════════════════════════════
source /srv/monorepo/.env

# ══ Mem0 ═════════════════════════════════════════════════════════════
MEM0_BACKEND=qdrant
MEM0_API_URL=http://localhost:8642

# ══ Qdrant (Gen5 NVMe /tank/qdrant) ════════════════════════════════
MEM0_QDRANT_URL=http://localhost:6333
MEM0_QDRANT_COLLECTION=will
QDRANT_API_KEY=${QDRANT_API_KEY}

# ══ Ollama (Gen5 NVMe /tank/models) ════════════════════════════════
MEM0_OLLAMA_URL=http://localhost:11434
MEM0_OLLAMA_MODEL=qwen2.5:3b

# ══ Tasks DB (Gen3 NVMe /srv/data/librarian) ════════════════════════
MEM0_TASKS_DB_PATH=/srv/data/librarian/tasks.db

# ══ MiniMax M2.7 (500 RPM) ════════════════════════════════════════════
MINIMAX_API_KEY=${MINIMAX_API_KEY}
MINIMAX_API_BASE=https://api.minimax.io
```

---

## Security Rules

### ✅ SAFE Operations
- Read from Mem0 collections (semantic search)
- Write to `will` collection (personal memories)
- Query task database
- Create/list collections via CollectionManager
- Backup collections before deletion

### ❌ FORBIDDEN
- Log API keys or secrets (echo, print, logging)
- Store credentials in code (use env vars)
- Expose Mem0 API port externally
- Delete collections without Archivist backup
- Use hardcoded API keys

---

## Collections (Qdrant)

| Collection | Instance | Vectors | Purpose |
|------------|----------|---------|---------|
| `will` | Hermes | 1973 | Personal memories |
| `second-brain` | Hermes | 79 | Knowledge graph |
| `mem0migrations` | Hermes | — | Migration history |
| `claude-code-memory` | Claude Code | — | CLI memories |
| `cursor-projects` | Cursor | — | IDE projects |
| `vscode-memory` | VS Code | — | Copilot data |
| `codex-repo` | Codex | — | CLI repos |

**Storage:** `/tank/qdrant/` (Gen5 NVMe — Crucial T700 4TB)

---

## Subagents

### MemoryArchivist
**Path:** `libs/subagents/memory_archivist.py`
**Spawned by:** Hermes as Python process

| Method | Purpose |
|--------|---------|
| `archive_old_memories(days=30)` | Tag old memories as archived |
| `compact_memories(max_per_user=100)` | Delete excess memories |
| `tag_memories(query, add_tags)` | Add tags to matching memories |
| `stats()` | Return collection statistics |

### CollectionManager
**Path:** `libs/subagents/collection_manager.py`
**Spawned by:** Hermes as Python process

| Method | Purpose |
|--------|---------|
| `create_collection(name, vector_size=768)` | Create Qdrant collection |
| `delete_collection(name)` | Delete collection |
| `list_collections()` | List all collections |
| `health_check()` | Verify Qdrant status |
| `stats()` | Return all collections statistics |

---

## Storage Topology

```
GEN5 NVMe (/tank — Crucial T700 4TB)
┌─────────────────────────────────────────────────────────────┐
│  /tank/qdrant/          7 Qdrant collections             │
│  /tank/models/          Ollama blobs (5.1GB)             │
│  /tank/docker-data/     Container persistent data          │
└─────────────────────────────────────────────────────────────┘

GEN3 NVMe (/dev/nvme1n1 — Kingston SNV3S 1TB)
┌─────────────────────────────────────────────────────────────┐
│  /                       OS + Coolify                       │
│  /home                   User home + configs               │
│  /srv/data/librarian/    SQLite tasks                       │
│  /srv/data/redis/        Redis (sessions, cache)           │
│  /srv/backups/           Backups                            │
└─────────────────────────────────────────────────────────────┘
```

---

## Incident Response

### Hermes Down
```bash
docker ps | grep hermes
docker logs hermes-second-brain --tail 50
docker restart hermes-second-brain
curl -sf http://localhost:8642/health
```

### Qdrant Slow
```bash
zpool status tank
iostat -x 5
curl -s -H "api-key: $QDRANT_API_KEY" http://localhost:6333/collections
```

### Ollama Unresponsive
```bash
curl -sf http://localhost:11434/api/tags | jq '.models'
docker restart ollama
```

---

## Audit Log

```bash
echo "$(date '+%Y-%m-%d %H:%M:%S') - Hermes Second Brain verified" >> /srv/logs/audit.log
```

---

**Monorepo:** `/srv/monorepo`
**Nexus:** `/srv/monorepo/.claude/vibe-kit/nexus.sh`
**Governance:** `/srv/monorepo/ops/ai-governance/`
