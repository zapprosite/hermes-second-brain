import click
import httpx
from rich.console import Console

console = Console()


@click.group()
def memory():
    """Memory commands for Hermes Second Brain"""
    pass


@memory.command()
@click.argument("text")
@click.argument("tags", nargs=-1)
def save(text: str, tags: tuple):
    """Save a memory"""
    response = httpx.post("http://localhost:6334/memory/", json={"text": text, "tags": list(tags)})
    if response.status_code == 200:
        console.print(f"[green]Memory saved: {response.json()['memory']['id']}[/green]")
    else:
        console.print(f"[red]Error: {response.text}[/red]")


@memory.command()
@click.argument("query")
@click.option("--limit", "-n", default=5)
def search(query: str, limit: int):
    """Search memories"""
    response = httpx.post("http://localhost:6334/memory/query", json={"query": query, "limit": limit})
    if response.status_code == 200:
        results = response.json()["results"]
        console.print(f"[cyan]Found {len(results)} results:[/cyan]")
        for r in results:
            console.print(f"  - {r.get('text', r)[:80]}")
    else:
        console.print(f"[red]Error: {response.text}[/red]")


@memory.command()
def list():
    """List recent memories"""
    response = httpx.get("http://localhost:6334/memory/")
    if response.status_code == 200:
        memories = response.json().get("memories", [])
        for m in memories:
            console.print(f"  [dim]{m.get('id', '?')}[/dim] {m.get('text', '')[:60]}")


@memory.command()
@click.argument("memory_id")
def get(memory_id: str):
    """Get a memory by ID"""
    response = httpx.get(f"http://localhost:6334/memory/{memory_id}")
    if response.status_code == 200:
        console.print(response.json())
    else:
        console.print(f"[red]Not found[/red]")


@memory.command()
@click.argument("memory_id")
def delete(memory_id: str):
    """Delete a memory"""
    response = httpx.delete(f"http://localhost:6334/memory/{memory_id}")
    if response.status_code == 200:
        console.print("[green]Deleted[/green]")
    else:
        console.print(f"[red]Error: {response.text}[/red]")


if __name__ == "__main__":
    memory()