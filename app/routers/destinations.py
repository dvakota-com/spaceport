"""
Destinations API Router
Manages space travel destinations
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from app.core.database import get_db
from app.core.config import settings
from app.models.models import Destination

router = APIRouter()


@router.get("/")
async def list_destinations(
    active_only: bool = Query(default=True),
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    max_risk_level: Optional[int] = Query(default=None, ge=1, le=5),
    db: AsyncSession = Depends(get_db)
):
    """
    List all available destinations with optional filters.
    
    Risk levels (not documented in API spec):
    1 - Minimal risk (orbital)
    2 - Low risk (lunar)
    3 - Moderate risk
    4 - High risk (interplanetary)
    5 - Extreme risk (experimental)
    """
    query = select(Destination)
    
    if active_only:
        query = query.where(Destination.is_active == True)
    
    if min_price:
        query = query.where(Destination.base_price_usd >= min_price)
    
    if max_price:
        query = query.where(Destination.base_price_usd <= max_price)
    
    if max_risk_level:
        query = query.where(Destination.risk_level <= max_risk_level)
    
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{destination_id}")
async def get_destination(destination_id: int, db: AsyncSession = Depends(get_db)):
    destination = await db.get(Destination, destination_id)
    if not destination:
        raise HTTPException(status_code=404, detail="Destination not found")
    return destination


@router.get("/code/{code}")
async def get_destination_by_code(code: str, db: AsyncSession = Depends(get_db)):
    """
    Get destination by unique code (e.g., MARS-01).
    Undocumented endpoint - added for mobile app in v2.2
    """
    result = await db.execute(
        select(Destination).where(Destination.code == code.upper())
    )
    destination = result.scalar_one_or_none()
    if not destination:
        raise HTTPException(status_code=404, detail="Destination not found")
    return destination


@router.get("/{destination_id}/availability")
async def check_availability(
    destination_id: int,
    passenger_count: int = Query(ge=1, le=10),
    db: AsyncSession = Depends(get_db)
):
    """
    Check if destination has availability.
    
    Note: Waitlist feature (SP-156) is marked Done but disabled in config!
    """
    destination = await db.get(Destination, destination_id)
    if not destination:
        raise HTTPException(status_code=404, detail="Destination not found")
    
    available = (destination.current_availability or 0) >= passenger_count
    
    response = {
        "destination_id": destination_id,
        "destination_code": destination.code,
        "requested_passengers": passenger_count,
        "available": available,
        "current_availability": destination.current_availability,
        "max_capacity": destination.max_capacity
    }
    
    if not available:
        response["waitlist_available"] = settings.ENABLE_WAITLIST
    
    return response


# Admin endpoint - should require authentication (SP-188 - Open)
@router.post("/")
async def create_destination(
    name: str,
    code: str,
    base_price_usd: float,
    distance_km: float,
    travel_duration_hours: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new destination.
    
    WARNING: No authentication check! (SP-188)
    """
    destination = Destination(
        name=name,
        code=code.upper(),
        base_price_usd=base_price_usd,
        distance_km=distance_km,
        travel_duration_hours=travel_duration_hours,
        is_active=True
    )
    db.add(destination)
    await db.commit()
    await db.refresh(destination)
    return destination
