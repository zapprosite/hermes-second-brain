from fastapi import FastAPI
from .router_memory import router as memory_router
from .router_tasks import router as tasks_router

app = FastAPI(title="Hermes Second Brain API", version="0.1.0")

app.include_router(memory_router, prefix="/memory", tags=["memory"])
app.include_router(tasks_router, prefix="/task", tags=["tasks"])


@app.get("/health")
def health():
    return {"status": "ok", "service": "hermes-second-brain"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=6334)