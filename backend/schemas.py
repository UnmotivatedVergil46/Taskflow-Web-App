"""Pydantic Schemas for Request/Response Validation"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Auth Schemas
class SignupRequest(BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    
    class Config:
        from_attributes = True

class AuthResponse(BaseModel):
    token: str
    user: UserResponse

# Task Schemas
class TaskCreate(BaseModel):
    title: str
    due_date: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    due_date: Optional[str] = None
    completed: Optional[bool] = None

class TaskResponse(BaseModel):
    id: int
    user_id: int
    title: str
    due_date: Optional[str] = None
    completed: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class ErrorResponse(BaseModel):
    error: str

class HealthResponse(BaseModel):
    status: str
    storage: str
    timestamp: str

class MessageResponse(BaseModel):
    message: str
