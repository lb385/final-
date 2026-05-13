"""FastAPI Backend for Calculator App with User Profile Management.

Features:
- User authentication with JWT tokens
- User profile management (create, read, update)
- Secure password management with bcrypt hashing
- Protected routes with bearer token authentication
- Comprehensive error handling and validation

Author: Development Team
Version: 1.0.0
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Optional

from database import get_db, engine
from models import Base, User
from schemas import (
    UserCreate, UserResponse, LoginRequest, Token, 
    UserUpdate, PasswordChange, CalculationBase, CalculationResponse
)
from security import hash_password, verify_password, create_access_token, verify_token
import models

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Calculator App with Profile Management",
    description="Full-stack application with user authentication and profile management",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper function to get current user from token
async def get_current_user(authorization: Optional[str] = None, db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header"
        )
    
    try:
        token = authorization.replace("Bearer ", "")
        payload = verify_token(token)
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        username: Optional[str] = payload.get("sub")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user

# ============ Authentication Routes ============

@app.post("/api/auth/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )
    
    # Create new user
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/api/auth/login", response_model=Token)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    """Login user and return access token."""
    user = db.query(User).filter(User.username == credentials.username).first()
    
    if not user or not verify_password(credentials.password, str(user.password_hash)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    access_token = create_access_token(data={"sub": user.username})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

# ============ Profile Routes ============

@app.get("/api/profile", response_model=UserResponse)
async def get_profile(
    authorization: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user profile."""
    return current_user

@app.put("/api/profile", response_model=UserResponse)
async def update_profile(
    update_data: UserUpdate,
    authorization: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update user profile information (username, email)."""
    
    # Check if new username/email already exists
    if update_data.username:
        existing = db.query(User).filter(
            (User.username == update_data.username) & (User.id != current_user.id)
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        setattr(current_user, 'username', update_data.username)
    
    if update_data.email:
        existing = db.query(User).filter(
            (User.email == update_data.email) & (User.id != current_user.id)
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already taken"
            )
        setattr(current_user, 'email', update_data.email)
    
    db.commit()
    db.refresh(current_user)
    return current_user

@app.post("/api/profile/change-password")
async def change_password(
    password_data: PasswordChange,
    authorization: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Change user password."""
    
    # Verify old password
    if not verify_password(password_data.old_password, str(current_user.password_hash)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Old password is incorrect"
        )
    
    # Check if new password and confirmation match
    if password_data.new_password != password_data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New passwords do not match"
        )
    
    # Update password
    setattr(current_user, 'password_hash', hash_password(password_data.new_password))
    db.commit()
    db.refresh(current_user)
    
    return {
        "message": "Password changed successfully",
        "user": current_user
    }

@app.delete("/api/account")
async def delete_account(
    authorization: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete user account permanently.
    
    WARNING: This action is irreversible. All user data will be deleted.
    
    Args:
        authorization: Bearer token for authentication
        db: Database session
        current_user: Authenticated user making the request
        
    Returns:
        dict: Confirmation message
        
    Raises:
        HTTPException: 401 if not authenticated
    """
    try:
        db.delete(current_user)
        db.commit()
        return {
            "message": "Account deleted successfully",
            "username": current_user.username
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete account"
        )

# ============ Health Check ============

@app.get("/health")
def health_check():
    """Health check endpoint for service monitoring.
    
    Returns:
        dict: Service status indicator
    """
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
