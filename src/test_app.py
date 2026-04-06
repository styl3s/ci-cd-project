import pytest
import json
from datetime import datetime
from app import create_app
from models import db, User, Task

@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture
def auth_headers(client):
    """Create user and return auth headers"""
    # Register user
    client.post('/api/auth/register', 
        json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123'
        },
        content_type='application/json'
    )
    
    # Login
    response = client.post('/api/auth/login', 
        json={
            'username': 'testuser',
            'password': 'testpass123'
        },
        content_type='application/json'
    )
    
    token = response.get_json()['access_token']
    return {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

# ==================== HEALTH CHECK TESTS ====================

def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {"status": "healthy"}

# ==================== AUTHENTICATION TESTS ====================

def test_register_user_success(client):
    """Test successful user registration"""
    response = client.post('/api/auth/register', json={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'password123'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['username'] == 'newuser'
    assert data['email'] == 'newuser@example.com'
    assert 'password' not in data

def test_register_missing_fields(client):
    """Test registration with missing fields"""
    response = client.post('/api/auth/register', json={
        'username': 'testuser'
    })
    assert response.status_code == 400
    assert 'error' in response.get_json()

def test_register_duplicate_username(client):
    """Test registration with duplicate username"""
    client.post('/api/auth/register', json={
        'username': 'duplicate',
        'email': 'user1@example.com',
        'password': 'pass123'
    })
    
    response = client.post('/api/auth/register', json={
        'username': 'duplicate',
        'email': 'user2@example.com',
        'password': 'pass456'
    })
    assert response.status_code == 400
    assert 'already exists' in response.get_json()['error']

def test_login_success(client):
    """Test successful login"""
    client.post('/api/auth/register', json={
        'username': 'loginuser',
        'email': 'login@example.com',
        'password': 'loginpass'
    })
    
    response = client.post('/api/auth/login', json={
        'username': 'loginuser',
        'password': 'loginpass'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'access_token' in data
    assert 'user' in data

def test_login_invalid_credentials(client):
    """Test login with invalid credentials"""
    response = client.post('/api/auth/login', json={
        'username': 'nonexistent',
        'password': 'wrongpass'
    })
    assert response.status_code == 401
    assert 'error' in response.get_json()

def test_login_missing_fields(client):
    """Test login with missing fields"""
    response = client.post('/api/auth/login', json={
        'username': 'testuser'
    })
    assert response.status_code == 400

# ==================== TASK CRUD TESTS ====================

def test_create_task_success(client, auth_headers):
    """Test successful task creation"""
    response = client.post('/api/tasks', 
        headers=auth_headers,
        json={
            'title': 'Test Task',
            'description': 'This is a test task',
            'priority': 'high',
            'status': 'todo'
        }
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == 'Test Task'
    assert data['priority'] == 'high'
    assert data['status'] == 'todo'

def test_create_task_missing_title(client, auth_headers):
    """Test task creation without title"""
    response = client.post('/api/tasks',
        headers=auth_headers,
        json={'description': 'No title'}
    )
    assert response.status_code == 400

def test_create_task_invalid_status(client, auth_headers):
    """Test task creation with invalid status"""
    response = client.post('/api/tasks',
        headers=auth_headers,
        json={
            'title': 'Task',
            'status': 'invalid_status'
        }
    )
    assert response.status_code == 400

def test_create_task_invalid_priority(client, auth_headers):
    """Test task creation with invalid priority"""
    response = client.post('/api/tasks',
        headers=auth_headers,
        json={
            'title': 'Task',
            'priority': 'invalid_priority'
        }
    )
    assert response.status_code == 400

def test_create_task_unauthorized(client):
    """Test task creation without authentication"""
    response = client.post('/api/tasks', json={
        'title': 'Unauthorized Task'
    })
    assert response.status_code == 401

def test_get_tasks_empty(client, auth_headers):
    """Test getting tasks when none exist"""
    response = client.get('/api/tasks', headers=auth_headers)
    assert response.status_code == 200
    assert response.get_json() == []

def test_get_tasks_with_data(client, auth_headers):
    """Test getting tasks with existing data"""
    client.post('/api/tasks', headers=auth_headers, json={
        'title': 'Task 1',
        'priority': 'high'
    })
    client.post('/api/tasks', headers=auth_headers, json={
        'title': 'Task 2',
        'priority': 'low'
    })
    
    response = client.get('/api/tasks', headers=auth_headers)
    assert response.status_code == 200
    tasks = response.get_json()
    assert len(tasks) == 2

def test_get_tasks_filtered_by_priority(client, auth_headers):
    """Test getting tasks filtered by priority"""
    client.post('/api/tasks', headers=auth_headers, json={
        'title': 'High Priority',
        'priority': 'high'
    })
    client.post('/api/tasks', headers=auth_headers, json={
        'title': 'Low Priority',
        'priority': 'low'
    })
    
    response = client.get('/api/tasks?priority=high', headers=auth_headers)
    assert response.status_code == 200
    tasks = response.get_json()
    assert len(tasks) == 1
    assert tasks[0]['priority'] == 'high'

def test_get_single_task(client, auth_headers):
    """Test getting a specific task"""
    create_response = client.post('/api/tasks', headers=auth_headers, json={
        'title': 'Specific Task'
    })
    task_id = create_response.get_json()['id']
    
    response = client.get(f'/api/tasks/{task_id}', headers=auth_headers)
    assert response.status_code == 200
    assert response.get_json()['title'] == 'Specific Task'

def test_get_nonexistent_task(client, auth_headers):
    """Test getting a task that doesn't exist"""
    response = client.get('/api/tasks/9999', headers=auth_headers)
    assert response.status_code == 404

def test_update_task_success(client, auth_headers):
    """Test successful task update"""
    create_response = client.post('/api/tasks', headers=auth_headers, json={
        'title': 'Original Title',
        'status': 'todo'
    })
    task_id = create_response.get_json()['id']
    
    response = client.put(f'/api/tasks/{task_id}', 
        headers=auth_headers,
        json={
            'title': 'Updated Title',
            'status': 'done'
        }
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'Updated Title'
    assert data['status'] == 'done'

def test_update_task_invalid_status(client, auth_headers):
    """Test updating task with invalid status"""
    create_response = client.post('/api/tasks', headers=auth_headers, json={
        'title': 'Task'
    })
    task_id = create_response.get_json()['id']
    
    response = client.put(f'/api/tasks/{task_id}',
        headers=auth_headers,
        json={'status': 'invalid'}
    )
    assert response.status_code == 400

def test_update_nonexistent_task(client, auth_headers):
    """Test updating a task that doesn't exist"""
    response = client.put('/api/tasks/9999',
        headers=auth_headers,
        json={'title': 'Updated'}
    )
    assert response.status_code == 404

def test_delete_task_success(client, auth_headers):
    """Test successful task deletion"""
    create_response = client.post('/api/tasks', headers=auth_headers, json={
        'title': 'Task to Delete'
    })
    task_id = create_response.get_json()['id']
    
    response = client.delete(f'/api/tasks/{task_id}', headers=auth_headers)
    assert response.status_code == 200
    
    get_response = client.get(f'/api/tasks/{task_id}', headers=auth_headers)
    assert get_response.status_code == 404

def test_delete_nonexistent_task(client, auth_headers):
    """Test deleting a task that doesn't exist"""
    response = client.delete('/api/tasks/9999', headers=auth_headers)
    assert response.status_code == 404

# ==================== AUTHORIZATION TESTS ====================

def test_user_can_only_see_own_tasks(client):
    """Test that users can only see their own tasks"""
    client.post('/api/auth/register', json={
        'username': 'user1',
        'email': 'user1@example.com',
        'password': 'pass1'
    })
    response1 = client.post('/api/auth/login', json={
        'username': 'user1',
        'password': 'pass1'
    })
    token1 = response1.get_json()['access_token']
    headers1 = {'Authorization': f'Bearer {token1}'}
    
    client.post('/api/auth/register', json={
        'username': 'user2',
        'email': 'user2@example.com',
        'password': 'pass2'
    })
    response2 = client.post('/api/auth/login', json={
        'username': 'user2',
        'password': 'pass2'
    })
    token2 = response2.get_json()['access_token']
    headers2 = {'Authorization': f'Bearer {token2}'}
    
    client.post('/api/tasks', headers=headers1, json={'title': 'User 1 Task'})
    
    response = client.get('/api/tasks', headers=headers2)
    assert len(response.get_json()) == 0