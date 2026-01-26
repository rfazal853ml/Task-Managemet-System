# Task Management System

A modern task management application built with FastAPI backend and vanilla HTML/CSS/JavaScript frontend. Perfect for testing DevOps pipelines.

## Features

- ✅ Create, read, update, and delete tasks
- 📊 Three-column kanban board (To Do, In Progress, Done)
- 🎨 Priority levels (Low, Medium, High)
- 🔍 Filter tasks by status
- 📱 Responsive design
- 🚀 RESTful API
- 🐳 Docker ready
- 💚 Health check endpoint

## Project Structure

```
task-management/
├── main.py                 # FastAPI backend
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose setup
├── .dockerignore          # Docker ignore file
├── static/
│   ├── index.html         # Frontend HTML
│   ├── styles.css         # CSS styles
│   └── app.js             # JavaScript logic
└── README.md
```

## Local Development

### Prerequisites

- Python 3.11+
- pip

### Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

4. Open your browser and navigate to:
```
http://localhost:8000
```

## Docker Deployment

### Build and run with Docker:

```bash
docker build -t task-management .
docker run -p 8000:8000 task-management
```

### Or use Docker Compose:

```bash
docker-compose up -d
```

## API Endpoints

### Health Check
- `GET /api/health` - Check API health status

### Tasks
- `GET /api/tasks` - Get all tasks (supports ?status=todo filter)
- `GET /api/tasks/{task_id}` - Get specific task
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/{task_id}` - Update task
- `DELETE /api/tasks/{task_id}` - Delete task

### Example API Request

```bash
# Create a task
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project",
    "description": "Finish the DevOps pipeline",
    "priority": "high",
    "status": "todo"
  }'

# Get all tasks
curl http://localhost:8000/api/tasks

# Health check
curl http://localhost:8000/api/health
```

## Testing the Application

### Manual Testing
1. Open the application in your browser
2. Add tasks with different priorities
3. Move tasks between columns by editing them
4. Delete completed tasks
5. Test filtering functionality

### API Testing
Use the `/api/health` endpoint for automated health checks in your pipeline:
```bash
curl -f http://localhost:8000/api/health || exit 1
```

## DevOps Pipeline Integration

This application is designed to be easy to integrate into CI/CD pipelines:

1. **Build Stage**: Build Docker image
2. **Test Stage**: Run health check against container
3. **Deploy Stage**: Deploy to your environment

### Example GitHub Actions Workflow

```yaml
name: CI/CD Pipeline

on: [push]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build Docker image
        run: docker build -t task-management .
      
      - name: Run container
        run: docker run -d -p 8000:8000 --name test-app task-management
      
      - name: Wait for startup
        run: sleep 5
      
      - name: Health check
        run: curl -f http://localhost:8000/api/health
      
      - name: Stop container
        run: docker stop test-app
```

## Environment Variables

The application can be configured with these environment variables:

- `ENV` - Environment name (default: production)
- Additional variables can be added as needed

## Performance

- Lightweight in-memory storage (suitable for testing)
- Fast response times
- Minimal resource usage
- Health check support for orchestration

## License

MIT License - Free to use for testing and development.

## Contributing

This is a sample application for DevOps pipeline testing. Feel free to modify and extend it for your needs!

