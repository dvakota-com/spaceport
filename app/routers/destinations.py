"""
Destinations API Router
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.models.models import Destination

router = APIRouter()

@router.get("/")
async def list_destinations(db: AsyncSession = Depends(get_db)):
    """List all available destinations"""
    result = await db.execute(select(Destination).where(Destination.is_active == True))
    return result.scalars().all()

@router.get("/{destination_id}")
async def get_destination(destination_id: int, db: AsyncSession = Depends(get_db)):
    destination = await db.get(Destination, destination_id)
    if not destination:
        raise HTTPException(status_code=404, detail="Destination not found")
    return destination
