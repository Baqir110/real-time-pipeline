# Real-Time Data Engineering Pipeline

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-green.svg)](https://fastapi.tiangolo.com/)
[![Pandas](https://img.shields.io/badge/pandas-2.0+-orange.svg)](https://pandas.pydata.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red.svg)](https://www.sqlalchemy.org/)
[![pytest](https://img.shields.io/badge/pytest-7.0+-yellow.svg)](https://docs.pytest.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](https://opensource.org/licenses/MIT)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [API Reference](#api-reference)
  - [Trigger ETL Pipeline](#post-apiv1trigger-etl)
  - [Retrieve Metrics](#get-apiv1metrics)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## 📖 Overview

A **production-grade data engineering pipeline** that ingests live public data, performs automated cleaning and validation, transforms datasets into business insights, persists aggregated metrics into a relational database, and exposes analytical endpoints via a RESTful API.

This project demonstrates end-to-end data engineering best practices, including:

- **ETL Automation**: Scheduled and on-demand data processing
- **Data Quality**: Schema validation, anomaly detection, and cleansing
- **Analytics**: Aggregated metrics and business intelligence ready for consumption
- **Observability**: Comprehensive logging and error handling

---

## 🏗️ Architecture

```mermaid
flowchart LR
    A[Public API\nJSONPlaceholder] --> B[Python Ingestion Module]
    B --> C[Pandas Validation &\nTransformation]
    C --> D[SQLAlchemy ORM]
    D --> E[Relational Database\nSQLite / PostgreSQL]
    E --> F[FastAPI REST\nAnalytics Endpoints]
    
    style A fill:#4CAF50,color:#fff
    style B fill:#2196F3,color:#fff
    style C fill:#FF9800,color:#fff
    style D fill:#9C27B0,color:#fff
    style E fill:#F44336,color:#fff
    style F fill:#00BCD4,color:#fff
```

### Data Flow

| Stage | Component | Description |
|-------|-----------|-------------|
| **Ingestion** | Python Module | Fetches real-time data from external sources |
| **Validation** | Pandas + Pydantic | Enforces schema integrity and data quality rules |
| **Transformation** | Pandas | Cleans anomalies, parses email domains, enriches records |
| **Storage** | SQLAlchemy ORM | Manages relational storage with automatic session handling |
| **Exposure** | FastAPI | Serves analytical insights via REST endpoints |

---

## ✨ Key Features

- **🔄 Automated ETL Pipeline**
  - Real-time external data fetching
  - Anomaly detection and data cleansing
  - Business insight extraction (e.g., email domain parsing)
  - Structured metric persistence

- **✅ Data Validation**
  - Pandas transformation pipelines
  - Pydantic model enforcement
  - Schema integrity checks

- **💾 Relational Storage**
  - SQLAlchemy ORM management
  - Automatic session handling
  - Migration support ready

- **🌐 RESTful API**
  - FastAPI backend with interactive Swagger UI (`/docs`)
  - JSON response formatting
  - Comprehensive error handling

- **🧪 Automated Testing**
  - Full integration test coverage
  - Endpoint validation using `pytest`
  - CI/CD ready

---

## 🛠️ Technology Stack

| Category | Technology | Version |
|----------|------------|---------|
| **Language** | Python | 3.8+ |
| **Web Framework** | FastAPI | 0.95+ |
| **Data Processing** | Pandas | 2.0+ |
| **ORM** | SQLAlchemy | 2.0+ |
| **Database** | SQLite / PostgreSQL | - |
| **Validation** | Pydantic | 2.0+ |
| **Testing** | Pytest | 7.0+ |
| **ASGI Server** | Uvicorn | 0.20+ |

---

## 📁 Project Structure

```plaintext
real-time-pipeline/
│
├── app/
│   ├── __init__.py
│   ├── main.py                # FastAPI application entry point
│   ├── config.py              # Configuration settings
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints.py       # REST API route definitions
│   │
│   ├── etl/
│   │   ├── __init__.py
│   │   └── pipeline.py        # ETL logic: ingestion, validation, transformation
│   │
│   └── models/
│       ├── __init__.py
│       └── database.py        # SQLAlchemy models & session management
│
├── data/
│   └── pipeline.db            # SQLite database file
│
├── tests/
│   ├── __init__.py
│   ├── test_api.py            # API endpoint tests
│   └── test_pipeline.py       # ETL pipeline tests
│
├── requirements.txt           # Project dependencies
├── .gitignore                 # Git ignore rules
└── README.md                  # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites

- **Python** 3.8 or higher
- **pip** (Python package manager)
- **Git** (for cloning the repository)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Baqir110/real-time-pipeline.git
   cd real-time-pipeline
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   ```

   **Windows (PowerShell):**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

   **macOS / Linux:**
   ```bash
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

### Running the Application

1. **Run automated tests** (optional but recommended)

   ```bash
   python -m pytest -v
   ```

2. **Start the application server**

   ```bash
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Access the API**

   - **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
   - **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 📚 API Reference

### `POST /api/v1/trigger-etl`

**Description**: Triggers the live ETL cycle — fetches external data, performs validation and transformation, and persists aggregated metrics to the database.

**Endpoint**: `POST /api/v1/trigger-etl`

**Request Body**: None

**Response Example**:
```json
{
  "status": "success",
  "timestamp": "2026-08-16T21:57:48.123456",
  "records_processed": 10,
  "unique_domains": 8,
  "message": "ETL pipeline executed successfully"
}
```

**Error Response**:
```json
{
  "status": "error",
  "timestamp": "2026-08-16T21:57:48.123456",
  "message": "Failed to fetch external data: Connection timeout"
}
```

---

### `GET /api/v1/metrics`

**Description**: Retrieves all aggregated analytical metrics stored in the pipeline database.

**Endpoint**: `GET /api/v1/metrics`

**Query Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `limit` | integer | No | Maximum number of records to return (default: 100) |
| `status` | string | No | Filter by status (e.g., "SUCCESS", "FAILED") |

**Response Example**:
```json
{
  "status": "success",
  "count": 2,
  "limit": 100,
  "data": [
    {
      "id": 1,
      "metric_name": "total_records_ingested",
      "value": 10.0,
      "status": "SUCCESS",
      "timestamp": "2026-08-16T21:57:48.123456"
    },
    {
      "id": 2,
      "metric_name": "unique_domains_extracted",
      "value": 8.0,
      "status": "SUCCESS",
      "timestamp": "2026-08-16T21:57:48.123456"
    }
  ]
}
```

---

## 🧪 Testing

The project includes comprehensive test coverage using `pytest`.

```bash
# Run all tests with verbose output
python -m pytest -v

# Run specific test file
python -m pytest tests/test_api.py -v

# Run tests with coverage report
python -m pytest --cov=app --cov-report=html
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow **PEP 8** style guidelines
- Write **docstrings** for all functions and classes
- Add **unit tests** for new functionality
- Ensure all tests pass before submitting a PR

---


## 📧 Contact

**Author**: Baqir110

**GitHub**: [github.com/Baqir110](https://github.com/Baqir110)

---

<p align="center">
  Made with ❤️ and 🐍 Python
</p>

<p align="center">
  ⭐ Star this repository if you find it useful!
</p>