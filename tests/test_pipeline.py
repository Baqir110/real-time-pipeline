from app.etl.pipeline import run_etl_pipeline

def test_run_etl_pipeline():
    result = run_etl_pipeline()
    assert result["status"] == "success"
    assert "records_processed" in result
    assert "unique_domains" in result
    assert result["records_processed"] > 0
