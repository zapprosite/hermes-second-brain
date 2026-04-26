# Hermes Second Brain

Memória persistente do Hermes Agent via Mem0 + Qdrant + SQLite.

## Quick Start

```bash
cd /srv/hermes-second-brain

# Setup virtualenv
python -m venv .venv && source .venv/bin/activate

# Install dependencies
pip install -e .

# Verify services
curl http://localhost:6333/health  # Qdrant
curl http://localhost:11434/api/tags  # Ollama

# Run API
cd apps/api && uvicorn main:app --reload --port 6334

# Or use CLI
python -m apps.cli.memory_commands --help
python -m apps.cli.task_commands --help
```

## Architecture

```
hermes-second-brain/
├── libs/memory/          # Mem0 wrapper
├── apps/api/             # FastAPI
├── apps/cli/             # CLI tools
├── skills/librarian/     # Hermes skill
└── services/qdrant/      # Qdrant config
```

## Commands

### /memory
- `python -m apps.cli.memory_commands save "texto" tag1 tag2`
- `python -m apps.cli.memory_commands search "pergunta"`
- `python -m apps.cli.memory_commands list`

### /task
- `python -m apps.cli.task_commands new "título"`
- `python -m apps.cli.task_commands list`
- `python -m apps.cli.task_commands done <id>`
- `python -m apps.cli.task_commands stats`