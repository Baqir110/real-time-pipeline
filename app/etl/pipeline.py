import logging
import pandas as pd
from datetime import datetime, timezone
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from app.models.database import PipelineMetric, init_db
from app.etl.ingestion import load_source_data

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# --- Pydantic Data Contract ---
class RawUserPayload(BaseModel):
    id: int
    name: str
    email: EmailStr
    username: str


class ETLResult(BaseModel):
    status: str
    timestamp: str
    records_processed: int
    unique_domains: int
    execution_time_ms: float


async def send_quality_alert(message: str, webhook_url: Optional[str] = None):
    """Logs and dispatches data quality alert notifications."""
    logger.error(f"[DATA QUALITY ALERT] {message}")


async def run_etl_pipeline_async(
    db: Session, source_type: str = "api", source_path: Optional[str] = None
) -> dict:
    """Executes ingestion, schema validation, transformation, and database load."""
    init_db()
    start_time = datetime.now(timezone.utc)

    # 1. Multi-Source Ingestion
    try:
        raw_data = await load_source_data(
            source_type=source_type, source_path=source_path
        )
        logger.info(f"Ingested {len(raw_data)} raw records from {source_type} source.")
    except Exception as e:
        error_msg = f"Ingestion failed ({source_type}): {str(e)}"
        await send_quality_alert(error_msg)
        return {"status": "error", "message": error_msg}

    # 2. Schema Validation via Pydantic Data Contracts
    validated_records = []
    dropped_count = 0
    for record in raw_data:
        try:
            validated_records.append(RawUserPayload(**record).model_dump())
        except Exception as val_err:
            dropped_count += 1
            logger.warning(f"Dropping invalid payload record: {val_err}")

    if dropped_count > 0:
        await send_quality_alert(
            f"Dropped {dropped_count} record(s) during Pydantic schema validation."
        )

    if not validated_records:
        error_msg = "No records passed schema validation contract."
        await send_quality_alert(error_msg)
        return {"status": "error", "message": error_msg}

    # 3. Data Transformation via Pandas
    df = pd.DataFrame(validated_records)
    total_records = len(df)
    df["email_domain"] = df["email"].apply(
        lambda x: str(x).split("@")[-1].lower() if "@" in str(x) else "unknown"
    )
    unique_domains = int(df["email_domain"].nunique())

    # 4. Database Persistence
    try:
        m1 = PipelineMetric(
            metric_name="total_records_ingested",
            value=float(total_records),
            status="SUCCESS",
        )
        m2 = PipelineMetric(
            metric_name="unique_email_domains",
            value=float(unique_domains),
            status="SUCCESS",
        )

        db.add_all([m1, m2])
        db.commit()
        logger.info("Successfully persisted ETL metrics to database.")
    except Exception as db_err:
        db.rollback()
        error_msg = f"Database insertion error: {db_err}"
        await send_quality_alert(error_msg)
        return {"status": "error", "message": error_msg}

    execution_time = (datetime.now(timezone.utc) - start_time).total_seconds() * 1000

    return ETLResult(
        status="success",
        timestamp=datetime.now(timezone.utc).isoformat(),
        records_processed=total_records,
        unique_domains=unique_domains,
        execution_time_ms=round(execution_time, 2),
    ).model_dump()
