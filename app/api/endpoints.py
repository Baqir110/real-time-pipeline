from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.database import SessionLocal, PipelineMetric
from app.etl.pipeline import run_etl_pipeline
from app.models.database import SessionLocal
# app/api/endpoints.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import SessionLocal, PipelineMetric, get_db

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/trigger-etl")
def trigger_pipeline():
    """Triggers the real-time ingestion, validation, and loading ETL pipeline."""
    result = run_etl_pipeline()
    return result

@router.get("/metrics")
def get_pipeline_metrics(db: Session = Depends(get_db)):
    """Retrieves all aggregated analytical metrics stored by the pipeline."""
    metrics = db.query(PipelineMetric).all()
    return {
        "status": "success",
        "count": len(metrics),
        "data": [
            {
                "id": m.id,
                "metric_name": m.metric_name,
                "value": m.value,
                "status": m.status,
                "timestamp": m.timestamp.isoformat()
            } for m in metrics
        ]
    }