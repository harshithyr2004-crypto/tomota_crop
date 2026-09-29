from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI(
    title="TomatoGuard AI",
    version="2.0.0"
)

ROOT = Path(__file__).resolve().parent.parent
FRONTEND = ROOT / "frontend"

if FRONTEND.exists():
    app.mount(
        "/static",
        StaticFiles(directory=str(FRONTEND)),
        name="static"
    )

@app.get("/")
async def home():
    return FileResponse(str(FRONTEND / "index.html"))

@app.get("/api/health")
async def health():
    return {
        "status": "healthy",
        "service": "TomatoGuard AI"
    }
