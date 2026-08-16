from fastapi import FastAPI
from app.config import settings
from app.api.endpoints import router as api_router
from app.models.database import init_db

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Initialize database tables on startup
@app.on_event("startup")
def startup_event():
    init_db()

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {"message": "Welcome to the Real-Time Data Engineering Pipeline API", "docs": "/docs"}