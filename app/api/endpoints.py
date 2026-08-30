from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.models.database import PipelineMetric, get_db
from app.etl.pipeline import run_etl_pipeline_async

router = APIRouter()


@router.post("/trigger-etl")
async def trigger_pipeline(db: Session = Depends(get_db)):
    """Triggers the real-time ingestion, validation, and loading ETL pipeline asynchronously."""
    result = await run_etl_pipeline_async(db)
    return result


@router.get("/metrics")
def get_pipeline_metrics(
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = None,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
):
    """Retrieves all aggregated analytical metrics stored by the pipeline."""
    query = db.query(PipelineMetric)

    if status:
        query = query.filter(PipelineMetric.status == status.upper())
    if from_date:
        query = query.filter(PipelineMetric.timestamp >= from_date)
    if to_date:
        query = query.filter(PipelineMetric.timestamp <= to_date)

    metrics = query.limit(limit).all()

    return {
        "status": "success",
        "count": len(metrics),
        "limit": limit,
        "data": [
            {
                "id": m.id,
                "metric_name": m.metric_name,
                "value": m.value,
                "status": m.status,
                "timestamp": m.timestamp.isoformat(),
            }
            for m in metrics
        ],
    }
