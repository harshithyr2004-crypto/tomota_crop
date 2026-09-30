import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKEND = ROOT / "backend"

sys.path.insert(0, str(BACKEND))

from app.main import app