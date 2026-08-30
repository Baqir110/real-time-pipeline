from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.endpoints import router as api_router
from app.config import settings
from app.models.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Real-Time Data Engineering Pipeline API"}