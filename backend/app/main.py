# -*- coding: utf-8 -*-
"""
TomatoGuard AI - Main FastAPI Application Entrypoint
"""

import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Ensure proper encoding in console
try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

from app.core.config import STATIC_FRONTEND_DIR
from app.routes.auth import router as auth_router
from app.routes.prediction import router as prediction_router
from app.routes.translation import router as translation_router
from app.routes.assistant import router as assistant_router
from app.routes.catalog import router as catalog_router

app = FastAPI(
    title="TomatoGuard AI - Crop Health & Disease Diagnosis Engine",
    description="Two-Stage Deep Learning Pipeline for Tomato Crop Verification & Disease Pathology",
    version="2.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(auth_router, prefix="/api", tags=["Authentication"])
app.include_router(prediction_router, prefix="/api", tags=["Two-Stage Prediction"])
app.include_router(translation_router, prefix="/api", tags=["Multilingual Translation"])
app.include_router(assistant_router, prefix="/api", tags=["Ask TomatoGuard AI"])
app.include_router(catalog_router, prefix="/api", tags=["Catalog & Health"])

# Mount Static Frontend
if STATIC_FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_FRONTEND_DIR)), name="static")

    @app.get("/", include_in_schema=False)
    async def serve_index():
        index_file = STATIC_FRONTEND_DIR / "index.html"
        if index_file.exists():
            return FileResponse(
                str(index_file),
                headers={
                    "Cache-Control": "no-cache, no-store, must-revalidate",
                    "Pragma": "no-cache",
                    "Expires": "0"
                }
            )
        return {"message": "TomatoGuard AI Backend Active. Open /docs for Swagger API."}


@app.get('/api/health')
async def health_check():
    return {'status': 'healthy', 'service': 'TomatoGuard AI', 'version': '2.0.0'}
