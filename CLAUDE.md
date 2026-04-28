# Hermes Second Brain — MEMORY LAYER

> **⚠️ READ FIRST:** This is part of the **HOMELAB MONOREPO** (`/srv/monorepo`)
> All infrastructure context is in `/srv/monorepo/HARDWARE_HIERARCHY.md`
>
> **Classification:** INTERNAL | **Owner:** Platform Engineering
> **Version:** 2.0.0 | **Updated:** 2026-04-26

---

## 🏠 Position in Homelab

```
/srv/monorepo/                          ← SINGLE SOURCE OF TRUTH
│
├── hermes-second-brain/                 ← YOU ARE HERE (Mem0 Memory)
│   ├── libs/
│   │   ├── subagents/                 # Python spawned processes
│   │   │   ├── memory_archivist.py   # Archive, compact, tag
│   │   │   └── collection_manager.py # Qdrant lifecycle
│   │   └── memory/
│   │       ├── config.py             # Settings
│   │       └── manager.py            # Mem0 client
│   ├── SOUL.md                        # Security & Architecture
│   └── docker-compose.yml              # Container config
│
├── ops/                               # IaC + Governance
├── hermes/                            # Hermes Agency (symlink)
└── apps/                              # Production services
```

---

## 🎯 Purpose

**Hermes Second Brain** is the **persistent memory layer** for all agents:

| Component | Technology | Purpose |
|-----------|------------|---------|
| Memory API | Mem0 (:8642) | Unified memory interface |
| Vector Store | Qdrant (:6333) | Semantic search storage |
| Embeddings | Ollama (:11434) | Local embedding generation |
| Cache | Redis (:6379) | Sessions & pub/sub |

---

## 🧠 Memory Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Hermes Second Brain                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐     │
│  │ MiniMax  │───▶│  Mem0    │◀───│  Hermes  │◀───│  Any    │     │
│  │  M2.7    │    │  API     │    │  Agent   │    │  Agent  │     │
│  │ (500RPM) │    │  :8642   │    │  :8642   │    │         │     │
│  └──────────┘    └────┬─────┘    └──────────┘    └──────────┘     │
│                      │                                               │
│                      ▼                                               │
│               ┌──────────────┐    ┌──────────────┐                  │
│               │   Qdrant     │◀───│   Ollama     │                  │
│               │   :6333      │    │   :11434    │                  │
│               │  7 Collections│    │  qwen2.5:3b │                  │
│               └──────────────┘    │ nomic-embed │                  │
│                                   └──────────────┘                  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📦 Collections (Qdrant — Gen5 NVMe)

| Collection | Vectors | Purpose | Status |
|------------|---------|---------|--------|
| `will` | 1973 | Personal memories | ✅ |
| `second-brain` | 79 | Knowledge graph | ✅ |
| `mem0migrations` | — | Migration history | ✅ |
| `claude-code-memory` | — | Claude CLI memories | ✅ |
| `cursor-projects` | — | Cursor IDE projects | ✅ |
| `vscode-memory` | — | VS Code Copilot | ✅ |
| `codex-repo` | — | Codex CLI repos | ✅ |

**Storage:** `/tank/qdrant/` (Gen5 NVMe — Crucial T700 4TB)

---

## 🔧 Subagents

Hermes spawns Python processes for specialized operations:

### MemoryArchivist
```python
from libs.subagents import MemoryArchivist

archivist = MemoryArchivist(collection="will")
archivist.archive_old_memories(days=30)
archivist.compact_memories(max_per_user=100)
archivist.tag_memories(query="projeto", add_tags=["important"])
archivist.stats()
```

### CollectionManager
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

## 🔐 Security

**Authoritative:** `/srv/monorepo/ops/ai-governance/CONTRACT.md`

### ✅ Safe
- Read/write to Mem0 collections
- Semantic search
- Collection management via subagents

### ❌ Forbidden
- Log API keys or secrets
- Hardcode credentials
- Delete collections without backup
- Expose port externally

---

## 🏥 Health Check

```bash
# Mem0 API
curl -sf http://localhost:8642/health

# Qdrant collections
curl -sf -H "api-key: $QDRANT_API_KEY" http://localhost:6333/collections | jq '.result.collections[].name'

# Ollama models
curl -sf http://localhost:11434/api/tags | jq '.models[].name'

# Full investigation
nexus-investigate.sh all 3
```

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `SOUL.md` | Security rules + architecture |
| `docker-compose.yml` | Container definition |
| `libs/subagents/memory_archivist.py` | Archive/compact/tag |
| `libs/subagents/collection_manager.py` | Qdrant lifecycle |
| `libs/memory/manager.py` | Mem0 client |

---

## 🚀 Quick Commands

```bash
# Enter container
docker exec -it hermes-second-brain bash

# View logs
docker logs hermes-second-brain --tail 50

# Restart
docker restart hermes-second-brain

# Check Qdrant vectors
curl -s -H "api-key: $QDRANT_API_KEY" http://localhost:6333/collections/will | jq '.result.vectors_count'
```

---

**Nexus:** `/srv/monorepo/.claude/vibe-kit/nexus.sh`
**Governance:** `/srv/monorepo/ops/ai-governance/`
**Monorepo:** `/srv/monorepo`
