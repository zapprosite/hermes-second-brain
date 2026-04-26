# Librarian Skill — Hermes Second Brain

## Trigger
`/memory` or `/task` commands in Hermes Agent

## When to Use
When Hermes needs to persist context, save important decisions, or manage tasks across sessions.

## Commands

### /memory save
Save a memory to Mem0 → Qdrant
```
/memory save <text> [tag1 tag2]
```

### /memory query
Semantic search in memory
```
/memory query <question>
```

### /memory list
List recent memories

### /memory get <id>
Retrieve specific memory

### /memory delete <id>
Delete a memory

### /task new <title>
Create new task (pending)

### /task list
List pending tasks

### /task done <id>
Mark task done

### /task stats
Show pending vs done

## Setup
```bash
pip install -e /srv/hermes-second-brain
```