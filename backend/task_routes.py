"""
Task Routes
-----------
GET    /api/tasks      — Get all tasks for the logged-in user
POST   /api/tasks      — Create a new task
PUT    /api/tasks/:id  — Update a task (title, due_date, or completed)
DELETE /api/tasks/:id  — Delete a task
"""

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List
from schemas import TaskCreate, TaskUpdate, TaskResponse, MessageResponse
from models import Task
from auth_utils import get_current_user
from config import get_db, is_using_memory, query_memory

router = APIRouter()

@router.get("", response_model=List[TaskResponse])
async def get_tasks(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get all tasks for the logged-in user."""
    try:
        user_id = current_user["id"]
        
        if is_using_memory():
            # Memory fallback
            tasks = query_memory(
                "SELECT * FROM tasks WHERE user_id = ? ORDER BY created_at DESC",
                [user_id]
            )
            return tasks
        else:
            # Database
            tasks = db.query(Task).filter(Task.user_id == user_id).order_by(Task.created_at.desc()).all()
            return tasks
    
    except Exception as e:
        print(f"Get tasks error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch tasks."
        )

@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(request: TaskCreate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Create a new task."""
    try:
        user_id = current_user["id"]
        title = request.title
        due_date = request.due_date
        
        if not title or title.strip() == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Task title is required."
            )
        
        if is_using_memory():
            # Memory fallback
            result = query_memory(
                "INSERT INTO tasks (user_id, title, due_date) VALUES (?, ?, ?)",
                [user_id, title.strip(), due_date]
            )
            task_id = result["insertId"]
            
            return TaskResponse(
                id=task_id,
                user_id=user_id,
                title=title.strip(),
                due_date=due_date,
                completed=False,
                created_at=__import__("datetime").datetime.utcnow()
            )
        else:
            # Database
            new_task = Task(
                user_id=user_id,
                title=title.strip(),
                due_date=due_date,
                completed=False
            )
            db.add(new_task)
            db.commit()
            db.refresh(new_task)
            return new_task
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Create task error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create task."
        )

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, request: TaskUpdate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Update a task."""
    try:
        user_id = current_user["id"]
        
        if is_using_memory():
            # Memory fallback
            existing = query_memory(
                "SELECT * FROM tasks WHERE id = ? AND user_id = ?",
                [task_id, user_id]
            )
            if not existing:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Task not found."
                )
            
            current = existing[0]
            updated_title = request.title.strip() if request.title else current["title"]
            updated_due_date = request.due_date if request.due_date is not None else current["due_date"]
            updated_completed = request.completed if request.completed is not None else current["completed"]
            
            query_memory(
                "UPDATE tasks SET title = ?, due_date = ?, completed = ? WHERE id = ? AND user_id = ?",
                [updated_title, updated_due_date, updated_completed, task_id, user_id]
            )
            
            return TaskResponse(
                id=current["id"],
                user_id=current["user_id"],
                title=updated_title,
                due_date=updated_due_date,
                completed=updated_completed,
                created_at=current["created_at"]
            )
        else:
            # Database
            task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
            if not task:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Task not found."
                )
            
            if request.title is not None:
                task.title = request.title.strip()
            if request.due_date is not None:
                task.due_date = request.due_date
            if request.completed is not None:
                task.completed = request.completed
            
            db.commit()
            db.refresh(task)
            return task
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Update task error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update task."
        )

@router.delete("/{task_id}", response_model=MessageResponse)
async def delete_task(task_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Delete a task."""
    try:
        user_id = current_user["id"]
        
        if is_using_memory():
            # Memory fallback
            result = query_memory(
                "DELETE FROM tasks WHERE id = ? AND user_id = ?",
                [task_id, user_id]
            )
            if result["affectedRows"] == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Task not found."
                )
            
            return MessageResponse(message="Task deleted successfully.")
        else:
            # Database
            task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
            if not task:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Task not found."
                )
            
            db.delete(task)
            db.commit()
            return MessageResponse(message="Task deleted successfully.")
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Delete task error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete task."
        )
