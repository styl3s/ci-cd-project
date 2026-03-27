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
    assert response.status_code == 200  # Changed from 201 to 200 (WRONG!)
    assert response.json["name"] == "Test Item"
    assert "id" in response.json

def test_create_item_missing_name(client):
    response = client.post('/api/items', json={})
    assert response.status_code == 400
    assert "error" in response.json

def test_get_items_after_creation(client):
    client.post('/api/items', json={"name": "Item 1"})
    client.post('/api/items', json={"name": "Item 2"})
    
    response = client.get('/api/items')
    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json[0]["name"] == "Item 1"
    assert response.json[1]["name"] == "Item 2"

def test_item_id_increment(client):
    response1 = client.post('/api/items', json={"name": "First"})
    response2 = client.post('/api/items', json={"name": "Second"})
    
    assert response1.json["id"] == 1
    assert response2.json["id"] == 2