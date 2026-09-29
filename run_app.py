# -*- coding: utf-8 -*-
"""
TomatoGuard AI - Full Stack Application Launcher
Runs the FastAPI backend and serves the interactive frontend on http://localhost:8000
"""

import sys
import os
from pathlib import Path

# Add backend directory to sys.path
BASE_DIR = Path(__file__).resolve().parent
BACKEND_DIR = BASE_DIR / "backend"
sys.path.insert(0, str(BACKEND_DIR))

try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

import uvicorn

def main():
    print("=" * 70)
    print("        🍅 TOMATOGUARD AI - TWO-STAGE CROP HEALTH SYSTEM 🍅        ")
    print("=" * 70)
    print("  Full-Stack Application is running at:")
    print("  -> 🌐 Web Application (Frontend) : http://localhost:8000")
    print("  -> 📖 Interactive API Docs       : http://localhost:8000/docs")
    print("  -> 🩺 System Health Endpoint      : http://localhost:8000/api/health")
    print("=" * 70)
    print("  Press Ctrl+C in this terminal to stop the server.")
    print("=" * 70)
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        app_dir=str(BACKEND_DIR)
    )

if __name__ == "__main__":
    main()
