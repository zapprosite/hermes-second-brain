# Hermes Second Brain — Enterprise Knowledge Management

**Location:** `/srv/hermes-second-brain`
**Purpose:** Mem0-backed knowledge graph for agents and Claude CLI integration
**Status:** OPERATIONAL | **Last Updated:** 2026-04-25

---

## Architecture

```
Internet → Cloudflare Tunnel → Home Lab
                              ↓
              ┌──────────────┼──────────────┐
              ↓              ↓              ↓
         gym.zappro.site  hermes.zappro.site  api.zappro.site
           (Docker)       (Python/Mem0)      (Python)
              ↓              ↓              ↓
         [:4010]          [:8642]          [:4000]
```

---

## Services

| Service | Port | Status | Health |
|---------|------|--------|--------|
| Hermes Agent | 8642 | ✅ ACTIVE | HTTP 200 |
| Mem0 | 8642 | ✅ ACTIVE | Connected |
| Qdrant | 6333 | ✅ ACTIVE | Vector DB |

---

## Nexus SRE Framework

**Scripts:** `/srv/monorepo/scripts/nexus-*.sh`

### Core Scripts

| Script | Purpose |
|--------|---------|
| `nexus-investigate.sh` | Deep health verification (4 layers) |
| `nexus-legacy-detector.sh` | Legacy/architecture violation detection |
| `nexus-alert.sh` | Persistent alerts with escalation |
| `nexus-context-window-manager.sh` | Context window monitoring |
| `nexus-tunnel.sh` | Tunnel ingress automation |
| `nexus-ufw.sh` | Firewall automation |
| `nexus-sre.sh` | Autonomous deploy system |
| `nexus-governance.sh` | Full deploy pipeline |

### Health Check

```bash
nexus-investigate.sh all 3
```

**Current:** 9/9 services healthy

---

## Directory Structure

### `/srv/` — Core Services

| Directory | Purpose | Status |
|-----------|---------|--------|
| `monorepo/` | Main monorepo (Nexus + Hermes + Mem0) | ✅ ACTIVE |
| `ops/` | Infrastructure as Code (Terraform) | ✅ ACTIVE |
| `hermes-second-brain/` | This repo - Knowledge management | ✅ ACTIVE |
| `fit-tracker-v2/` | Fitness tracking application | ✅ ACTIVE |
| `hvacr-swarm/` | HVAC automation | ✅ ACTIVE |
| `edge-tts/` | Edge TTS service | ✅ ACTIVE |
| `data/` | Persistent data volumes | ✅ ACTIVE |
| `backups/` | Backup storage | ✅ ACTIVE |
| `docker-data/` | Docker volumes | ✅ ACTIVE |
| `models/` | Ollama models | ✅ ACTIVE |
| `archive/` | Archived projects | ✅ ORGANIZED |

### `/srv/archive/`

- `apps.monitoring/` — Orphaned Prometheus/Grafana config
- `hvac/` — Empty HVAC project

### `/home/will/` — Development Environment

| Directory | Purpose | Status |
|-----------|---------|--------|
| `pc-cel/` | RustDesk remote control | ✅ ACTIVE |
| `go/` | Go modules (gentle-ai, gopls) | ✅ ACTIVE |
| `dev/skills/` | Homelab skills (anti-prompt-injection, etc) | ✅ ACTIVE |
| `mcp-data/memory-keeper/` | Context database | ✅ ACTIVE |
| `obsidian-vault/` | Personal notes | ✅ ACTIVE |
| `.local/bin/codex` | Codex CLI binary | ✅ ACTIVE |

### Archived (`/home/will/*.archive`)

- `Documents.archive/` — Old project docs
- `Desktop/docs.archive/` — Old SPECs and docs

---

## Service Health Matrix

| Service | URL | Port | Container | Status |
|---------|-----|------|-----------|--------|
| Gym MVP | gym.zappro.site | 4010 | docker | ✅ |
| Hermes Agent | hermes.zappro.site | 8642 | python | ✅ |
| API Gateway | api.zappro.site | 4000 | python | ✅ |
| Chat Service | chat.zappro.site | 3456 | python | ✅ |
| LLM Gateway | llm.zappro.site | 4002 | node | ✅ |
| Qdrant DB | qdrant.zappro.site | 6333 | qdrant | ✅ |
| Coolify | coolify.zappro.site | 8000 | php | ✅ |
| Gitea Git | git.zappro.site | 3300 | gitea | ✅ |
| PGAdmin | pgadmin.zappro.site | 4050 | docker | ✅ |

---

## Cron Jobs

| Schedule | Command | Purpose |
|----------|---------|---------|
| `*/5 * * * *` | `nexus-investigate.sh all 3` | Health check |
| `*/30 * * * *` | `nexus-cron-legacy.sh scan` | Legacy scan |
| `0 * * * *` | `nexus-cron-helper.sh status` | Status report |

---

## Governance Rules

### Safe Operations (No Approval)
- Read-only operations (logs, status, inspection)
- Backups and snapshots
- Documentation updates
- Application development in `/srv/monorepo`

### Requires Approval
- Service restart/stop/start
- Package installation/upgrade
- ZFS operations
- Firewall changes
- Network modifications

### Forbidden
- Disk wipe operations
- Delete `/srv/data`, `/srv/backups`
- ZFS pool destruction
- Exposing ports without updating PORTS.md + SUBDOMAINS.md

---

## Legacy Detection

```bash
# Full scan
nexus-legacy-detector.sh full /srv/monorepo

# Current status
✅ 0 architecture violations
✅ 0 empty files
✅ 9/9 services healthy
```

---

## Escalation Matrix

| Level | Response Time | Contact | Action |
|-------|---------------|---------|--------|
| P1 Critical | 15 min | On-call | Full outage, data loss risk |
| P2 High | 1 hour | Platform Team | Service degradation |
| P3 Medium | 4 hours | SRE on-duty | Non-critical issue |
| P4 Low | 24 hours | Next business day | Documentation, cleanup |

---

**Nexus Framework:** 7 modes × 7 agents = 49 specializations
**Entry:** `nexus.sh --mode <mode>`
**Docs:** `/srv/monorepo/docs/NEXUS-SRE-GUIDE.md`
