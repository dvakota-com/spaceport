"""
Bookings API Router
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
import uuid

from app.core.database import get_db
from app.models.models import Booking, BookingStatus, Destination

router = APIRouter()

MAX_TRAVELERS_PER_BOOKING = 6  # Per PRD requirements

@router.post("/")
async def create_booking(
    user_id: int,
    destination_id: int,
    departure_date: datetime,
    return_date: datetime,
    num_travelers: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Create new booking.
    Max 6 travelers per booking as per PRD-2024-Q2.
    """
    if num_travelers > MAX_TRAVELERS_PER_BOOKING:
        raise HTTPException(status_code=400, detail=f"Maximum {MAX_TRAVELERS_PER_BOOKING} travelers allowed")
    
    destination = await db.get(Destination, destination_id)
    if not destination:
        raise HTTPException(status_code=404, detail="Destination not found")
    
    # Calculate price (basic - will be enhanced in SP-120)
    final_amount = destination.base_price_usd * num_travelers
    
    booking = Booking(
        reference_code=f"SP-{uuid.uuid4().hex[:8].upper()}",
        user_id=user_id,
        destination_id=destination_id,
        departure_date=departure_date,
        return_date=return_date,
        num_travelers=num_travelers,
        final_amount=final_amount,
        status=BookingStatus.PENDING
    )
    
    db.add(booking)
    await db.commit()
    await db.refresh(booking)
    
    return booking

@router.get("/{booking_id}")
async def get_booking(booking_id: int, db: AsyncSession = Depends(get_db)):
    booking = await db.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@router.put("/{booking_id}")
async def update_booking(booking_id: int, db: AsyncSession = Depends(get_db)):
    """Update booking. Only PENDING bookings can be modified."""
    booking = await db.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    if booking.status != BookingStatus.PENDING:
        raise HTTPException(status_code=400, detail="Only pending bookings can be modified")
    
    # Update logic here
    return booking
