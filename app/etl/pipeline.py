import requests
import pandas as pd
from datetime import datetime
from app.models.database import SessionLocal, PipelineMetric, init_db

def run_etl_pipeline():
    # Ensure tables exist
    init_db()
    
    # 1. Ingestion: Fetch data from a public placeholder API (e.g., JSONPlaceholder Users)
    try:
        response = requests.get("https://jsonplaceholder.typicode.com/users", timeout=10)
        response.raise_for_status()
        raw_data = response.json()
    except Exception as e:
        print(f"Ingestion failed: {e}")
        return {"status": "error", "message": str(e)}

    # 2. Validation & Transformation via Pandas
    df = pd.DataFrame(raw_data)
    
    # Simple transformation: Count records, extract domains from emails, check status
    total_records = len(df)
    df['email_domain'] = df['email'].apply(lambda x: x.split('@')[-1] if '@' in x else 'unknown')
    active_domains_count = df['email_domain'].nunique()

    # 3. Load / Persistence into database
    db = SessionLocal()
    try:
        # Save metrics
        metric_1 = PipelineMetric(metric_name="total_records_ingested", value=float(total_records), status="SUCCESS")
        metric_2 = PipelineMetric(metric_name="unique_email_domains", value=float(active_domains_count), status="SUCCESS")
        
        db.add(metric_1)
        db.add(metric_2)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Database load failed: {e}")
        return {"status": "error", "message": str(e)}
    finally:
        db.close()

    return {
        "status": "success",
        "timestamp": datetime.utcnow().isoformat(),
        "records_processed": total_records,
        "unique_domains": active_domains_count
    }