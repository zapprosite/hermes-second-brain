# P0 — QDRANT_API_KEY Rotation Required

- **Date:** 2026-04-28
- **Severity:** P0 (SECRET EXPOSTO EM HISTÓRICO GIT)
- **Status:** Open

## Finding

docker-compose.yml:29 contenha QDRANT_API_KEY real commitada em 2026-04-21. Corrigido em 0aca835 para usar ${QDRANT_API_KEY}. Porem o valor real continua no histórico git (Gitea + GitHub mirror).

## Action Required

Rotacao da QDRANT_API_KEY no Qdrant e renovacao em todos os consumers (.env files, Coolify, etc.)

## Steps

1. Gerar nova QDRANT_API_KEY
2. Atualizar /srv/ops/secrets/hermes-qdrant.env (QDRANT_API_KEY=newvalue)
3. Restart Qdrant container (docker compose down/up)
4. Atualizar todos os consumers
5. Validar no Gitea + GitHub mirror que historico nao contem a nova key

## Affected Services

- hermes-second-brain
- monorepo smoke-tests
- HVAC-RAG pipeline

## References

- commit 0aca835
- docker-compose.yml
