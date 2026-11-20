from fastapi import FastAPI

from app.routers import health, practice

app = FastAPI(title="Cab App")

app.include_router(health.router)
app.include_router(practice.router)
