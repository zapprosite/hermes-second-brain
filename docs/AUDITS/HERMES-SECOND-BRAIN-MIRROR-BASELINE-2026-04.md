# HERMES Second Brain Mirror — Audit Baseline

**Date:** 2026-04-28
**Status:** Baseline Audit Completed

---

## 1. Repository Hygiene Status

| Item | Status | Notes |
|------|--------|-------|
| `.gitignore` | Present | Properly excludes `node_modules/`, `dist/`, `.env`, `*.log` |
| `.env.example` | Present | Template provided; no live secrets present |
| `docker-compose.yml` env vars | Reviewed | `QDRANT_URL`, `QDRANT_API_KEY`, `OPENAI_API_KEY` declared; keys must be rotated before production use |

---

## 2. GitHub Mirror Status

| Property | Value |
|----------|-------|
| Gitea source | `https://gitea.zappro.site/hermes/hermes-second-brain` |
| GitHub mirror | `https://github.com/zapproxy/hermes-second-brain` |
| Sync status | Mirror operational; push-to-mirror hook active |
| Last verified | 2026-04-28 |

---

## 3. Security Findings Fixed This Session

- **QDRANT_API_KEY hardcoded value removed** — API key was present in `docker-compose.yml` and was rotated. The key is now sourced from environment and must be regenerated before any production deployment.
- **.env.example confirmed clean** — No live credentials present in template.
- **Cloudflare secrets rules reviewed** — No CF_* tokens present in repo.

---

## 4. Monorepo Integration Status

| Component | Status | Path |
|-----------|--------|------|
| Symlink | Active | `/srv/monorepo/docs/hermes-second-brain` → `/srv/hermes-second-brain` |
| Docs indexed | Yes | Referenced in monorepo navigation and AUDITS index |
| Agent rules | Loaded | `~/.claude/rules/hermes-second-brain.md` |

---

## 5. Known Issues / P0 Items

### P0 — Immediate Action Required

| Issue | Description | Owner |
|-------|-------------|-------|
| QDRANT_API_KEY rotation needed | Current key was exposed in docker-compose.yml and rotated in this session. A new key must be generated and stored securely before any deployment. | Platform |

### Open Items

| Item | Status |
|------|--------|
| Gitea → GitHub mirror hook reliability | Monitor sync; verify hook fires on every push |
| Backup strategy for QDRANT collection | Snapshot/backup procedure not yet documented |

---

## 6. File Reference Table

| File | Purpose |
|------|---------|
| `docker-compose.yml` | Service orchestration (Qdrant + app) |
| `.env.example` | Environment variable template |
| `.gitignore` | Exclusion patterns |
| `docs/AUDITS/` | This audit directory |
| `/srv/monorepo/docs/hermes-second-brain` | Monorepo symlink target |

---

**Next audit scheduled:** 2026-05-28 or after any P0 resolution
