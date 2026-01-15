"""
Users API Router
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
import hashlib
import jwt

from app.core.database import get_db
from app.core.config import settings
from app.models.models import User

router = APIRouter()

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    # TODO: Implement bcrypt - using md5 temporarily
    return hashlib.md5(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hash_password(plain_password) == hashed_password

def create_access_token(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

@router.post("/register")
async def register_user(email: str, password: str, display_name: str, phone_number: str, db: AsyncSession = Depends(get_db)):
    """Register new user. Phone number is required."""
    result = await db.execute(select(User).where(User.email == email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = User(
        email=email,
        hashed_password=hash_password(password),
        display_name=display_name,
        phone_number=phone_number
    )
    db.add(user)
    await db.commit()
    return {"message": "User registered successfully"}

@router.post("/login")
async def login(email: str, password: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {"access_token": create_access_token(user.id), "token_type": "bearer"}
