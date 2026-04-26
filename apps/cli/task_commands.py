import click
import httpx
from rich.console import Console

console = Console()


@click.group()
def task():
    """Task board commands for Hermes Second Brain"""
    pass


@task.command()
@click.argument("title")
@click.option("--project")
@click.option("--tags")
def new(title: str, project: str, tags: str):
    """Create a new task"""
    response = httpx.post("http://localhost:6334/task/", json={"title": title, "project": project, "tags": tags})
    if response.status_code == 200:
        console.print(f"[green]Task created: #{response.json()['id']}[/green]")


@task.command()
@click.option("--status")
def list(status: str):
    """List tasks"""
    params = {"status": status} if status else {}
    response = httpx.get("http://localhost:6334/task/", params=params)
    if response.status_code == 200:
        tasks = response.json().get("tasks", [])
        for t in tasks:
            console.print(f"  [dim]# {t['id']}[/dim] [{t['status']}] {t['title']}")


@task.command()
@click.argument("task_id", type=int)
def done(task_id: int):
    """Mark task as done"""
    response = httpx.post(f"http://localhost:6334/task/{task_id}/done")
    if response.status_code == 200:
        console.print(f"[green]Task #{task_id} marked done[/green]")


@task.command()
@click.argument("task_id", type=int)
@click.argument("title")
def edit(task_id: int, title: str):
    """Edit task title"""
    response = httpx.patch(f"http://localhost:6334/task/{task_id}", json={"title": title})
    if response.status_code == 200:
        console.print(f"[green]Task #{task_id} updated[/green]")


@task.command()
@click.argument("task_id", type=int)
def delete(task_id: int):
    """Delete a task"""
    response = httpx.delete(f"http://localhost:6334/task/{task_id}")
    if response.status_code == 200:
        console.print("[green]Deleted[/green]")


@task.command()
def stats():
    """Show task statistics"""
    response = httpx.get("http://localhost:6334/task/stats")
    if response.status_code == 200:
        stats = response.json()
        console.print(f"Pending: [yellow]{stats['pending']}[/yellow], Done: [green]{stats['done']}[/green]")


if __name__ == "__main__":
    task()