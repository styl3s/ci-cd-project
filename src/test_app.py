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

def test_get_items_empty(client):
    response = client.get('/api/items')
    assert response.status_code == 200
    assert response.json == []

def test_create_item_success(client):
    response = client.post('/api/items', json={"name": "Test Item"})
    assert response.status_code == 201
    assert response.json["name"] == "Test Item"
    assert "id" in response.json




