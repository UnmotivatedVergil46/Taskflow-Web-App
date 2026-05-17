# Todo App Backend (Python)

A modern REST API backend built with FastAPI for the Todo Web Application, converted from Node.js/Express.

## Features

- **User Authentication**: JWT-based auth with bcrypt password hashing
- **Task Management**: Full CRUD operations for tasks
- **Database Support**: MySQL with optional in-memory fallback for development
- **Async Support**: FastAPI's async/await for high performance
- **CORS Enabled**: Ready for frontend integration
- **Health Check**: Endpoint to verify server status and storage backend

## Tech Stack

- **Framework**: FastAPI (async, fast, modern)
- **ORM**: SQLAlchemy (for database abstraction)
- **Auth**: PyJWT + Passlib with bcrypt
- **Database**: MySQL 5.7+ (with in-memory fallback)
- **Server**: Uvicorn (ASGI server)

## Project Structure

```
backend/
├── main.py              # Entry point and app setup
├── config.py            # Database configuration
├── models.py            # SQLAlchemy ORM models
├── schemas.py           # Pydantic request/response schemas
├── auth_utils.py        # JWT token generation and verification
├── auth_routes.py       # Authentication endpoints
├── task_routes.py       # Task management endpoints
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables
├── setup.sql            # Database schema (MySQL)
└── README.md           # This file
```

## Installation

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

Edit `.env` file with your settings:

```env
PORT=5000
JWT_SECRET=your-secret-key-change-in-production
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your-password
DB_NAME=todo_app
```

### 3. Setup Database (Optional)

If using MySQL, run the SQL setup script:

```bash
mysql -u root -p < setup.sql
```

If MySQL is unavailable, the app will automatically fall back to in-memory storage.

## Running the Server

### Development

```bash
python main.py
```

The server will start on `http://localhost:5000`

### Production

```bash
uvicorn main:app --host 0.0.0.0 --port 5000 --workers 4
```

## API Endpoints

### Authentication

- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - Login and get JWT token

### Tasks (Require Authentication)

- `GET /api/tasks` - Get all user's tasks
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task

### System

- `GET /api/health` - Health check (shows storage status)

## Request/Response Examples

### Signup

**Request:**
```json
POST /api/auth/signup
{
  "username": "john_doe",
  "password": "secure_password"
}
```

**Response:**
```json
{
  "token": "eyJhbGc...",
  "user": {
    "id": 1,
    "username": "john_doe"
  }
}
```

### Create Task

**Request:**
```json
POST /api/tasks
Authorization: Bearer <token>
{
  "title": "Complete project",
  "due_date": "2024-12-31"
}
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "title": "Complete project",
  "due_date": "2024-12-31",
  "completed": false,
  "created_at": "2024-05-17T10:00:00"
}
```

## Validation Rules

- **Username**: Minimum 3 characters, must be unique
- **Password**: Minimum 6 characters
- **Task Title**: Cannot be empty
- **JWT Token**: Expires in 7 days

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message"
}
```

HTTP Status Codes:
- `400` - Bad Request (validation error)
- `401` - Unauthorized (invalid credentials or token)
- `409` - Conflict (username already exists)
- `404` - Not Found (task or user not found)
- `500` - Internal Server Error

## Database Schema

### Users Table
```sql
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tasks Table
```sql
CREATE TABLE tasks (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  title VARCHAR(255) NOT NULL,
  due_date DATE,
  completed BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

## Migration from Node.js

This Python backend maintains 100% API compatibility with the original Express.js backend. No frontend changes are required to use this version.

### Key Differences

- **Async by Default**: FastAPI uses async/await (better performance)
- **Better Type Hints**: Pydantic for automatic validation
- **Simpler Middleware**: Decorator-based authentication
- **ORM Models**: Type-safe database interactions
- **Zero Database Overhead**: Same in-memory fallback as Node version

## Development Tips

### Running with Auto-Reload

```bash
uvicorn main:app --reload
```

### Testing with cURL

```bash
# Signup
curl -X POST http://localhost:5000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "password": "test123"}'

# Get tasks
curl http://localhost:5000/api/tasks \
  -H "Authorization: Bearer <token>"
```

### Using Python Interactive Shell

```python
import requests
resp = requests.post("http://localhost:5000/api/auth/login", 
                     json={"username": "test", "password": "test123"})
token = resp.json()["token"]
```

## Troubleshooting

### MySQL Connection Error

If you see "MySQL connection failed", the app will use in-memory storage automatically.

To enable MySQL:
1. Ensure MySQL is running
2. Check DB_HOST, DB_USER, DB_PASSWORD in `.env`
3. Run `setup.sql` to create database and tables

### Port Already in Use

Change the `PORT` in `.env` or use:
```bash
PORT=3000 python main.py
```

### ImportError Issues

Ensure you're running from the correct directory:
```bash
cd backend
python main.py
```

## License

Same as the main project.
