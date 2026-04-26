from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import sqlite3
from libs.memory.config import settings

router = APIRouter()


def get_db():
    conn = sqlite3.connect(settings.tasks_db_path)
    conn.row_factory = sqlite3.Row
    return conn


class TaskCreate(BaseModel):
    title: str
    project: Optional[str] = None
    tags: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None


@router.post("/")
def create_task(input: TaskCreate):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO tasks (title, project, tags) VALUES (?, ?, ?)",
        (input.title, input.project, input.tags),
    )
    conn.commit()
    task_id = cur.lastrowid
    conn.close()
    return {"success": True, "id": task_id}


@router.get("/")
def list_tasks(status: Optional[str] = None):
    conn = get_db()
    cur = conn.cursor()
    if status:
        rows = cur.execute("SELECT * FROM tasks WHERE status = ? ORDER BY created_at DESC", (status,)).fetchall()
    else:
        rows = cur.execute("SELECT * FROM tasks ORDER BY created_at DESC").fetchall()
    conn.close()
    return {"tasks": [dict(r) for r in rows]}


@router.patch("/{task_id}")
def update_task(task_id: int, input: TaskUpdate):
    conn = get_db()
    cur = conn.cursor()
    if input.title:
        cur.execute("UPDATE tasks SET title = ?, updated_at = ? WHERE id = ?", (input.title, datetime.now().isoformat(), task_id))
    conn.commit()
    conn.close()
    return {"success": True}


@router.post("/{task_id}/done")
def mark_done(task_id: int):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET status = 'done', done_at = ? WHERE id = ?", (datetime.now().isoformat(), task_id))
    conn.commit()
    conn.close()
    return {"success": True}


@router.delete("/{task_id}")
def delete_task(task_id: int):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return {"success": True}


@router.get("/stats")
def task_stats():
    conn = get_db()
    cur = conn.cursor()
    pending = cur.execute("SELECT COUNT(*) FROM tasks WHERE status = 'pending'").fetchone()[0]
    done = cur.execute("SELECT COUNT(*) FROM tasks WHERE status = 'done'").fetchone()[0]
    conn.close()
    return {"pending": pending, "done": done}