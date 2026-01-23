from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uvicorn

app = FastAPI(title="Task Management API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

## Comment for jenkins git trigger test ##

# In-memory database
tasks_db = []
task_id_counter = 1

class Task(BaseModel):
    title: str
    description: Optional[str] = ""
    status: str = "todo"  # todo, in-progress, done
    priority: str = "medium"  # low, medium, high
    
class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    priority: str
    created_at: str

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None

@app.get("/")
async def root():
    return FileResponse("static/index.html")

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/api/tasks", response_model=List[TaskResponse])
async def get_tasks(status: Optional[str] = None):
    if status:
        return [t for t in tasks_db if t["status"] == status]
    return tasks_db

@app.get("/api/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int):
    task = next((t for t in tasks_db if t["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/api/tasks", response_model=TaskResponse, status_code=201)
async def create_task(task: Task):
    global task_id_counter
    new_task = {
        "id": task_id_counter,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "priority": task.priority,
        "created_at": datetime.now().isoformat()
    }
    tasks_db.append(new_task)
    task_id_counter += 1
    return new_task

@app.put("/api/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, task_update: TaskUpdate):
    task = next((t for t in tasks_db if t["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task_update.title is not None:
        task["title"] = task_update.title
    if task_update.description is not None:
        task["description"] = task_update.description
    if task_update.status is not None:
        task["status"] = task_update.status
    if task_update.priority is not None:
        task["priority"] = task_update.priority
    
    return task

@app.delete("/api/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int):
    global tasks_db
    task = next((t for t in tasks_db if t["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks_db = [t for t in tasks_db if t["id"] != task_id]
    return None

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)