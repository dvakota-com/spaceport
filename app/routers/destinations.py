"""
Destinations API Router
"""

from fastapi import APIRouter
from typing import List

router = APIRouter()


@router.get("/")
async def list_destinations():
    """List all available destinations"""
    return []


@router.get("/{destination_id}")
async def get_destination(destination_id: int):
    """Get destination details"""
    return {"id": destination_id}
