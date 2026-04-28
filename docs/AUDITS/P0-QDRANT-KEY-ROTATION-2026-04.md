# P0 — QDRANT_API_KEY Rotation Required

- **Date:** 2026-04-28
- **Severity:** P0 (SECRET EXPOSTO EM HISTÓRICO GIT)
- **Status:** RESOLVED (2026-04-28)

## Finding

docker-compose.yml:29 contenha QDRANT_API_KEY real commitada em 2026-04-21. Corrigido em 0aca835 para usar ${QDRANT_API_KEY}. Porem o valor real continua no histórico git (Gitea + GitHub mirror).

## Action Required

Rotacao da QDRANT_API_KEY no Qdrant e renovacao em todos os consumers (.env files, Coolify, etc.)

## Steps (COMPLETED)

1. ✅ Gerar nova QDRANT_API_KEY — `e42076f3eeeabd45e...`
2. ✅ Atualizar /srv/monorepo/.env — canonical source (gitignored)
3. ✅ Restart Qdrant container — hermes-second-brain-qdrant-1
4. ✅ Atualizar todos os consumers — 9 docker-compose files com env_file: /srv/monorepo/.env
5. ✅ Validar Qdrant funcional com nova key — 9 colecções acessíveis

## Affected Services

- hermes-second-brain
- monorepo smoke-tests
- HVAC-RAG pipeline

## References

- commit 0aca835
- docker-compose.yml
