# P0 — QDRANT_API_KEY Rotation Required

- **Date:** 2026-04-28
- **Severity:** P0 (SECRET EXPOSTO EM HISTÓRICO GIT)
- **Status:** RESOLVED (2026-04-28)

## Finding

docker-compose.yml:29 continha QDRANT_API_KEY real commitada em 2026-04-21. Corrigido em 0aca835 para usar ${QDRANT_API_KEY}. Porém o valor real continua no histórico git (Gitea + GitHub mirror).

**SEGUNDA ROTAÇÃO (2026-04-28):** Primeira key nova (`e42076f3...`) foi inadvertidamente exposta em output Claude Code CLI durante sessão. Nova rotação aplicada. Regra `docs/OPERATIONS/SECRETS-PATTERNS.md` criada.

## Action Required

Rotação da QDRANT_API_KEY no Qdrant e renovação em todos os consumers.

## Steps (COMPLETED)

1. ✅ QDRANT_API_KEY rotacionada — valor nunca impresso em output
2. ✅ Atualizar /srv/monorepo/.env — canonical source (gitignored)
3. ✅ Restart Qdrant container — hermes-second-brain-qdrant-1
4. ✅ Atualizar todos os consumers — 9 docker-compose files com env_file: /srv/monorepo/.env
5. ✅ Validar Qdrant funcional — 9 colecções acessíveis

## Nova Regra

`docs/OPERATIONS/SECRETS-PATTERNS.md` — todas as variáveis de segredo documentadas com padrão seguro.

## Affected Services

- hermes-second-brain
- monorepo smoke-tests
- HVAC-RAG pipeline

## References

- commit 0aca835
- docs/OPERATIONS/SECRETS-PATTERNS.md
