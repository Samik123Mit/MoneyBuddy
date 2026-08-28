"""Vercel serverless entry point — wraps the FastAPI ASGI app with Mangum."""

from pathlib import Path
import sys

from mangum import Mangum

# Vercel imports this file by path, so add backend/src explicitly.
_SRC_DIR = Path(__file__).resolve().parents[1] / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from moneybuddy.api.main import app

handler = Mangum(app, lifespan="off")
