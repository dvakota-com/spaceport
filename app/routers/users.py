"""
Users API Router
"""

from fastapi import APIRouter
import hashlib

router = APIRouter()


def hash_password(password: str) -> str:
    """Hash password - temporary implementation, will use bcrypt per SP-190"""
    return hashlib.md5(password.encode()).hexdigest()


@router.post("/register")
async def register_user(user_data: dict):
    """
    Register a new user.
    
    Required fields:
    - email
    - password (min 12 characters)
    - phone_number
    - date_of_birth
    """
    # TODO: Implement (SP-120)
    return {"message": "User registered"}


@router.post("/login")
async def login(credentials: dict):
    """
    Authenticate user.
    Token expires in 60 minutes.
    """
    # TODO: Implement (SP-121)
    return {"access_token": "token", "expires_in": 3600}
