"""
Authentication Routes
---------------------
POST /api/auth/signup  — Register a new user
POST /api/auth/login   — Login and get a JWT token
"""

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import bcrypt
from schemas import SignupRequest, LoginRequest, AuthResponse, UserResponse, ErrorResponse
from models import User
from auth_utils import generate_token
from config import get_db, is_using_memory, query_memory

router = APIRouter()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(10)).decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash."""
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

@router.post("/signup", response_model=AuthResponse)
async def signup(request: SignupRequest, db: Session = Depends(get_db)):
    """Register a new user."""
    try:
        username = request.username
        password = request.password
        
        # Validate input
        if not username or not password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username and password are required."
            )
        if len(username) < 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username must be at least 3 characters."
            )
        if len(password) < 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 6 characters."
            )
        
        # Check if using memory or database
        if is_using_memory():
            # Memory fallback
            result = query_memory("SELECT * FROM users WHERE username = ?", [username])
            if result:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Username already taken."
                )
            
            password_hash = hash_password(password)
            result = query_memory("INSERT INTO users (username, password_hash) VALUES (?, ?)", 
                                [username, password_hash])
            user_id = result["insertId"]
            token = generate_token(user_id, username)
            
            return AuthResponse(
                token=token,
                user=UserResponse(id=user_id, username=username)
            )
        else:
            # Database
            existing = db.query(User).filter(User.username == username).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Username already taken."
                )
            
            password_hash = hash_password(password)
            new_user = User(username=username, password_hash=password_hash)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            token = generate_token(new_user.id, new_user.username)
            
            return AuthResponse(
                token=token,
                user=UserResponse(id=new_user.id, username=new_user.username)
            )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Signup error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error during signup."
        )

@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Login and get JWT token."""
    try:
        username = request.username
        password = request.password
        
        # Validate input
        if not username or not password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password."
            )
        
        # Check if using memory or database
        if is_using_memory():
            # Memory fallback
            users = query_memory("SELECT * FROM users WHERE username = ?", [username])
            if not users:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid username or password."
                )
            
            user = users[0]
            if not verify_password(password, user["password_hash"]):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid username or password."
                )
            
            token = generate_token(user["id"], user["username"])
            return AuthResponse(
                token=token,
                user=UserResponse(id=user["id"], username=user["username"])
            )
        else:
            # Database
            user = db.query(User).filter(User.username == username).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid username or password."
                )
            
            if not verify_password(password, user.password_hash):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid username or password."
                )
            
            token = generate_token(user.id, user.username)
            return AuthResponse(
                token=token,
                user=UserResponse(id=user.id, username=user.username)
            )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error during login."
        )
