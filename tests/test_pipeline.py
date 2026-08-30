import pytest
from app.etl.pipeline import run_etl_pipeline_async
from app.models.database import SessionLocal, init_db


@pytest.mark.asyncio
async def test_run_etl_pipeline_async():
    init_db()
    db = SessionLocal()
    try:
        result = await run_etl_pipeline_async(db)
        assert result["status"] == "success"
        assert "records_processed" in result
        assert "unique_domains" in result
        assert result["records_processed"] > 0
        assert "execution_time_ms" in result
    finally:
        db.close()
