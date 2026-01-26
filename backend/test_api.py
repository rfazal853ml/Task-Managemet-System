import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "healthy"

def test_get_tasks_empty():
    """Test getting tasks when database is empty"""
    response = client.get("/api/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_task():
    """Test creating a new task"""
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "status": "todo",
        "priority": "high"
    }
    response = client.post("/api/tasks", json=task_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert data["status"] == task_data["status"]
    assert data["priority"] == task_data["priority"]
    assert "id" in data
    assert "created_at" in data

def test_get_task_by_id():
    """Test getting a specific task"""
    # Create a task first
    task_data = {
        "title": "Get Task Test",
        "description": "Test getting task by ID",
        "status": "todo",
        "priority": "medium"
    }
    create_response = client.post("/api/tasks", json=task_data)
    task_id = create_response.json()["id"]
    
    # Get the task
    response = client.get(f"/api/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == task_data["title"]

def test_get_task_not_found():
    """Test getting a non-existent task"""
    response = client.get("/api/tasks/99999")
    assert response.status_code == 404

def test_update_task():
    """Test updating a task"""
    # Create a task first
    task_data = {
        "title": "Original Title",
        "description": "Original description",
        "status": "todo",
        "priority": "low"
    }
    create_response = client.post("/api/tasks", json=task_data)
    task_id = create_response.json()["id"]
    
    # Update the task
    update_data = {
        "title": "Updated Title",
        "status": "in-progress",
        "priority": "high"
    }
    response = client.put(f"/api/tasks/{task_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["status"] == update_data["status"]
    assert data["priority"] == update_data["priority"]

def test_update_task_not_found():
    """Test updating a non-existent task"""
    update_data = {"title": "Updated"}
    response = client.put("/api/tasks/99999", json=update_data)
    assert response.status_code == 404

def test_delete_task():
    """Test deleting a task"""
    # Create a task first
    task_data = {
        "title": "Task to Delete",
        "description": "This task will be deleted",
        "status": "todo",
        "priority": "medium"
    }
    create_response = client.post("/api/tasks", json=task_data)
    task_id = create_response.json()["id"]
    
    # Delete the task
    response = client.delete(f"/api/tasks/{task_id}")
    assert response.status_code == 204
    
    # Verify it's deleted
    get_response = client.get(f"/api/tasks/{task_id}")
    assert get_response.status_code == 404

def test_delete_task_not_found():
    """Test deleting a non-existent task"""
    response = client.delete("/api/tasks/99999")
    assert response.status_code == 404

def test_filter_tasks_by_status():
    """Test filtering tasks by status"""
    # Create tasks with different statuses
    client.post("/api/tasks", json={"title": "Todo Task", "status": "todo", "priority": "low"})
    client.post("/api/tasks", json={"title": "In Progress Task", "status": "in-progress", "priority": "medium"})
    client.post("/api/tasks", json={"title": "Done Task", "status": "done", "priority": "high"})
    
    # Filter by status
    response = client.get("/api/tasks?status=todo")
    assert response.status_code == 200
    tasks = response.json()
    assert all(task["status"] == "todo" for task in tasks)

def test_create_task_validation():
    """Test task creation with missing required fields"""
    response = client.post("/api/tasks", json={})
    assert response.status_code == 422  # Validation error

def test_task_priority_levels():
    """Test all priority levels"""
    priorities = ["low", "medium", "high"]
    for priority in priorities:
        task_data = {
            "title": f"Task with {priority} priority",
            "priority": priority,
            "status": "todo"
        }
        response = client.post("/api/tasks", json=task_data)
        assert response.status_code == 201
        assert response.json()["priority"] == priority

def test_task_status_levels():
    """Test all status levels"""
    statuses = ["todo", "in-progress", "done"]
    for status in statuses:
        task_data = {
            "title": f"Task with {status} status",
            "status": status,
            "priority": "medium"
        }
        response = client.post("/api/tasks", json=task_data)
        assert response.status_code == 201
        assert response.json()["status"] == status

def test_multiple_tasks():
    """Test creating and retrieving multiple tasks"""
    # Create multiple tasks
    for i in range(5):
        task_data = {
            "title": f"Task {i}",
            "description": f"Description {i}",
            "status": "todo",
            "priority": "medium"
        }
        client.post("/api/tasks", json=task_data)
    
    # Get all tasks
    response = client.get("/api/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) >= 5