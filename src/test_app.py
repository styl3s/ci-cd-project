import pytest
from app import app, items

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        items.clear()
        yield client

def test_health_endpoint(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {"status": "healthy"}








