from contextlib import asynccontextmanager
from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.api.endpoints import router as api_router
from app.config import settings
from app.models.database import init_db, SessionLocal
from app.etl.pipeline import run_etl_pipeline_async

scheduler = AsyncIOScheduler()

async def scheduled_etl_job():
    db = SessionLocal()
    try:
        await run_etl_pipeline_async(db)
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    # Run ETL every 5 minutes
    scheduler.add_job(scheduled_etl_job, 'interval', minutes=5)
    scheduler.start()
    yield
    scheduler.shutdown()

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Real-Time Data Engineering Pipeline API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}