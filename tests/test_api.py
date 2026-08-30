from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get('/')
    assert response.status_code == 200
    assert 'Real-Time Data Engineering Pipeline' in response.json()['message']

def test_health():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'healthy'

def test_trigger_etl():
    response = client.post('/api/v1/trigger-etl')
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'success'
    assert 'records_processed' in data

def test_get_metrics():
    response = client.get('/api/v1/metrics')
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'success'
    assert 'count' in data
    assert isinstance(data['data'], list)
