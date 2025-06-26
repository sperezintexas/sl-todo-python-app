from fastapi.testclient import TestClient
from server import app
import pytest

client = TestClient(app)

def test_create_todo():
    response = client.post(
        "/todos/",
        json={"title": "Test todo", "description": "Test description", "completed": False}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test todo"
    assert data["description"] == "Test description"
    assert data["completed"] == False
    assert "id" in data

def test_get_todos():
    # First, create a todo
    client.post(
        "/todos/",
        json={"title": "Test todo", "description": "Test description", "completed": False}
    )
    
    response = client.get("/todos/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_single_todo():
    # First, create a todo
    create_response = client.post(
        "/todos/",
        json={"title": "Test todo", "description": "Test description", "completed": False}
    )
    todo_id = create_response.json()["id"]
    
    # Then get it
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == todo_id
    assert data["title"] == "Test todo"

def test_update_todo():
    # First, create a todo
    create_response = client.post(
        "/todos/",
        json={"title": "Test todo", "description": "Test description", "completed": False}
    )
    todo_id = create_response.json()["id"]
    
    # Update it
    response = client.put(
        f"/todos/{todo_id}",
        json={"title": "Updated todo", "description": "Updated description", "completed": True}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated todo"
    assert data["completed"] == True

def test_delete_todo():
    # First, create a todo
    create_response = client.post(
        "/todos/",
        json={"title": "Test todo", "description": "Test description", "completed": False}
    )
    todo_id = create_response.json()["id"]
    
    # Delete it
    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 200
    
    # Verify it's gone
    get_response = client.get(f"/todos/{todo_id}")
    assert get_response.status_code == 404

def test_get_nonexistent_todo():
    response = client.get("/todos/123e4567-e89b-12d3-a456-426614174000")
    assert response.status_code == 404

def test_invalid_todo_data():
    response = client.post(
        "/todos/",
        json={"wrong_field": "Test todo"}  # Missing required fields
    )
    assert response.status_code == 422  # Validation error