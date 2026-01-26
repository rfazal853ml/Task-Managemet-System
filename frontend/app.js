// Use environment-based API URL
const API_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:8000/api'
    : 'https://task-managemet-system-production.up.railway.app/api';

let currentFilter = 'all';

// DOM elements
const taskForm = document.getElementById('taskForm');
const editTaskForm = document.getElementById('editTaskForm');
const modal = document.getElementById('editModal');
const closeModal = document.querySelector('.close');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadTasks();
    setupEventListeners();
});

// Event listeners
function setupEventListeners() {
    taskForm.addEventListener('submit', handleAddTask);
    editTaskForm.addEventListener('submit', handleEditTask);
    closeModal.addEventListener('click', () => modal.style.display = 'none');
    
    window.addEventListener('click', (e) => {
        if (e.target === modal) modal.style.display = 'none';
    });
    
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            currentFilter = e.target.dataset.filter;
            loadTasks();
        });
    });
}

// Load tasks
async function loadTasks() {
    try {
        const url = currentFilter === 'all' 
            ? `${API_URL}/tasks`
            : `${API_URL}/tasks?status=${currentFilter}`;
        
        const response = await fetch(url);
        const tasks = await response.json();
        
        renderTasks(tasks);
    } catch (error) {
        console.error('Error loading tasks:', error);
        showNotification('Failed to load tasks', 'error');
    }
}

// Render tasks
function renderTasks(tasks) {
    const todoContainer = document.getElementById('todoTasks');
    const inProgressContainer = document.getElementById('inProgressTasks');
    const doneContainer = document.getElementById('doneTasks');
    
    todoContainer.innerHTML = '';
    inProgressContainer.innerHTML = '';
    doneContainer.innerHTML = '';
    
    if (tasks.length === 0) {
        const emptyState = `
            <div class="empty-state">
                <div class="empty-state-icon">🔭</div>
                <p>No tasks yet</p>
            </div>
        `;
        todoContainer.innerHTML = emptyState;
        return;
    }
    
    tasks.forEach(task => {
        const taskCard = createTaskCard(task);
        
        switch(task.status) {
            case 'todo':
                todoContainer.appendChild(taskCard);
                break;
            case 'in-progress':
                inProgressContainer.appendChild(taskCard);
                break;
            case 'done':
                doneContainer.appendChild(taskCard);
                break;
        }
    });
    
    // Show empty state for empty columns
    if (todoContainer.children.length === 0) {
        todoContainer.innerHTML = '<div class="empty-state"><div class="empty-state-icon">🔭</div></div>';
    }
    if (inProgressContainer.children.length === 0) {
        inProgressContainer.innerHTML = '<div class="empty-state"><div class="empty-state-icon">🔭</div></div>';
    }
    if (doneContainer.children.length === 0) {
        doneContainer.innerHTML = '<div class="empty-state"><div class="empty-state-icon">🔭</div></div>';
    }
}

// Create task card
function createTaskCard(task) {
    const card = document.createElement('div');
    card.className = 'task-card';
    
    const priorityClass = `priority-${task.priority}`;
    const date = new Date(task.created_at).toLocaleDateString();
    
    card.innerHTML = `
        <div class="task-header">
            <div class="task-title">${escapeHtml(task.title)}</div>
            <span class="priority-badge ${priorityClass}">${task.priority}</span>
        </div>
        ${task.description ? `<div class="task-description">${escapeHtml(task.description)}</div>` : ''}
        <div class="task-actions">
            <button class="btn-small btn-edit" onclick="openEditModal(${task.id})">Edit</button>
            <button class="btn-small btn-delete" onclick="deleteTask(${task.id})">Delete</button>
        </div>
        <div class="task-meta">Created: ${date}</div>
    `;
    
    return card;
}

// Add task
async function handleAddTask(e) {
    e.preventDefault();
    
    const title = document.getElementById('taskTitle').value;
    const description = document.getElementById('taskDescription').value;
    const priority = document.getElementById('taskPriority').value;
    
    try {
        const response = await fetch(`${API_URL}/tasks`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, description, priority, status: 'todo' })
        });
        
        if (response.ok) {
            taskForm.reset();
            loadTasks();
            showNotification('Task added successfully!', 'success');
        }
    } catch (error) {
        console.error('Error adding task:', error);
        showNotification('Failed to add task', 'error');
    }
}

// Open edit modal
async function openEditModal(taskId) {
    try {
        const response = await fetch(`${API_URL}/tasks/${taskId}`);
        const task = await response.json();
        
        document.getElementById('editTaskId').value = task.id;
        document.getElementById('editTaskTitle').value = task.title;
        document.getElementById('editTaskDescription').value = task.description || '';
        document.getElementById('editTaskPriority').value = task.priority;
        document.getElementById('editTaskStatus').value = task.status;
        
        modal.style.display = 'block';
    } catch (error) {
        console.error('Error loading task:', error);
        showNotification('Failed to load task', 'error');
    }
}

// Edit task
async function handleEditTask(e) {
    e.preventDefault();
    
    const taskId = document.getElementById('editTaskId').value;
    const title = document.getElementById('editTaskTitle').value;
    const description = document.getElementById('editTaskDescription').value;
    const priority = document.getElementById('editTaskPriority').value;
    const status = document.getElementById('editTaskStatus').value;
    
    try {
        const response = await fetch(`${API_URL}/tasks/${taskId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, description, priority, status })
        });
        
        if (response.ok) {
            modal.style.display = 'none';
            loadTasks();
            showNotification('Task updated successfully!', 'success');
        }
    } catch (error) {
        console.error('Error updating task:', error);
        showNotification('Failed to update task', 'error');
    }
}

// Delete task
async function deleteTask(taskId) {
    if (!confirm('Are you sure you want to delete this task?')) return;
    
    try {
        const response = await fetch(`${API_URL}/tasks/${taskId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            loadTasks();
            showNotification('Task deleted successfully!', 'success');
        }
    } catch (error) {
        console.error('Error deleting task:', error);
        showNotification('Failed to delete task', 'error');
    }
}

// Utility functions
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showNotification(message, type) {
    // Simple console notification - you can enhance this with a proper notification UI
    console.log(`[${type.toUpperCase()}] ${message}`);
}