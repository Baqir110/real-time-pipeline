import os
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Float, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

# Ensure SQLite target directory exists
db_path = settings.DATABASE_URL.replace("sqlite:///", "")
if db_path and not db_path.startswith(":memory:"):
    db_dir = os.path.dirname(os.path.abspath(db_path))
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class PipelineMetric(Base):
    __tablename__ = "pipeline_metrics"

    id = Column(Integer, primary_key=True, index=True)
    metric_name = Column(String, index=True)
    value = Column(Float, nullable=True)
    status = Column(String, nullable=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)