"""Vercel serverless entry point — wraps the FastAPI ASGI app with Mangum."""

from mangum import Mangum

from moneybuddy.api.main import app

handler = Mangum(app, lifespan="off")
