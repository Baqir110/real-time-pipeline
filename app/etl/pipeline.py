import logging
import httpx
import pandas as pd
from datetime import datetime, timezone
from typing import List
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from app.models.database import PipelineMetric, init_db

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
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


async def fetch_external_data_async(url: str, timeout: float = 10.0) -> List[dict]:
    """Fetches payload asynchronously with strict timeout handling."""
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()


async def run_etl_pipeline_async(db: Session) -> dict:
    """Executes asynchronous ingestion, schema validation, transformation, and load."""
    init_db()
    start_time = datetime.now(timezone.utc)

    # 1. Ingestion
    try:
        raw_json = await fetch_external_data_async("https://jsonplaceholder.typicode.com/users")
        logger.info(f"Ingested {len(raw_json)} raw records from external source.")
    except Exception as e:
        logger.error(f"Ingestion failure: {str(e)}")
        return {"status": "error", "message": f"Ingestion failed: {str(e)}"}

    # 2. Validation via Pydantic Data Contracts
    validated_records = []
    for record in raw_json:
        try:
            validated_records.append(RawUserPayload(**record).model_dump())
        except Exception as val_err:
            logger.warning(f"Dropping invalid payload record: {val_err}")

    if not validated_records:
        return {"status": "error", "message": "No records passed validation contract."}

    # 3. Transformation via Pandas
    df = pd.DataFrame(validated_records)
    total_records = len(df)
    df["email_domain"] = df["email"].apply(lambda x: str(x).split("@")[-1].lower() if "@" in str(x) else "unknown")
    unique_domains = int(df["email_domain"].nunique())

    # 4. Load / Persistence
    try:
        m1 = PipelineMetric(metric_name="total_records_ingested", value=float(total_records), status="SUCCESS")
        m2 = PipelineMetric(metric_name="unique_email_domains", value=float(unique_domains), status="SUCCESS")

        db.add_all([m1, m2])
        db.commit()
        logger.info("Successfully persisted ETL metrics to database.")
    except Exception as db_err:
        db.rollback()
        logger.error(f"Database insertion error: {db_err}")
        return {"status": "error", "message": str(db_err)}

    execution_time = (datetime.now(timezone.utc) - start_time).total_seconds() * 1000

    return ETLResult(
        status="success",
        timestamp=datetime.now(timezone.utc).isoformat(),
        records_processed=total_records,
        unique_domains=unique_domains,
        execution_time_ms=round(execution_time, 2)
    ).model_dump()