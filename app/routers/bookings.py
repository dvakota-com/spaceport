"""
Bookings API Router
Handles all booking-related operations
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
import uuid

from app.core.database import get_db
from app.core.config import settings
from app.models.models import Booking, BookingStatus, Destination
from app.services.pricing import PricingService
from app.services.notifications import send_booking_confirmation

router = APIRouter()


@router.post("/")
async def create_booking(
    user_id: int,
    destination_id: int,
    departure_date: datetime,
    return_date: datetime = None,
    passenger_count: int = 1,
    discount_code: str = None,
    special_requests: str = None,
    # seat_class: str = "economy",  # SP-203: Coming soon
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new space travel booking.
    
    Business Rules (per PRD-2024-Q2):
    - Maximum 6 passengers per booking
    - Early bird discount: 10% for bookings 90+ days ahead
    - Minimum age: 21 years
    """
    if passenger_count > settings.MAX_PASSENGERS_PER_BOOKING:
        raise HTTPException(
            status_code=400,
            detail=f"Maximum {settings.MAX_PASSENGERS_PER_BOOKING} passengers allowed"
        )
    
    destination = await db.get(Destination, destination_id)
    if not destination:
        raise HTTPException(status_code=404, detail="Destination not found")
    
    if destination.current_availability and destination.current_availability < passenger_count:
        raise HTTPException(status_code=400, detail="Not enough availability")
    
    pricing_service = PricingService()
    price_breakdown = pricing_service.calculate_total(
        base_price=destination.base_price_usd,
        passenger_count=passenger_count,
        departure_date=departure_date,
        discount_code=discount_code
    )
    
    reference_code = f"SP-{uuid.uuid4().hex[:8].upper()}"
    
    booking = Booking(
        reference_code=reference_code,
        user_id=user_id,
        destination_id=destination_id,
        departure_date=departure_date,
        return_date=return_date,
        passenger_count=passenger_count,
        total_price=price_breakdown["total"],
        discount_applied=price_breakdown["discount"],
        discount_code=discount_code,
        status=BookingStatus.PENDING,
        special_requests=special_requests
    )
    
    db.add(booking)
    await db.commit()
    await db.refresh(booking)
    
    if destination.current_availability:
        destination.current_availability -= passenger_count
        await db.commit()
    
    # Send confirmation (async, fire-and-forget)
    # BUG: This should await, notifications sometimes not sent (SP-211)
    send_booking_confirmation(booking.id)
    
    return booking


@router.get("/{booking_id}")
async def get_booking(booking_id: int, db: AsyncSession = Depends(get_db)):
    booking = await db.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


@router.put("/{booking_id}")
async def update_booking(
    booking_id: int,
    special_requests: str = None,
    db: AsyncSession = Depends(get_db)
):
    """Update booking. Only PENDING bookings can be modified (per SP-134)."""
    booking = await db.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # Actually allows CONFIRMED too - inconsistent with docs
    if booking.status not in [BookingStatus.PENDING, BookingStatus.CONFIRMED]:
        raise HTTPException(status_code=400, detail="Only pending or confirmed bookings can be modified")
    
    if special_requests:
        booking.special_requests = special_requests
    
    booking.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(booking)
    
    return booking


@router.post("/{booking_id}/cancel")
async def cancel_booking(booking_id: int, db: AsyncSession = Depends(get_db)):
    """
    Cancel a booking.
    
    Cancellation Policy (per Terms v3.1):
    - More than 30 days: Full refund minus 20% fee
    - 15-30 days: 50% refund
    - Less than 15 days: No refund
    """
    booking = await db.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    if booking.status == BookingStatus.CANCELLED:
        raise HTTPException(status_code=400, detail="Booking already cancelled")
    
    days_until_departure = (booking.departure_date - datetime.utcnow()).days
    
    if days_until_departure > 30:
        refund_percent = 100 - settings.CANCELLATION_FEE_PERCENT  # 75%, not 80%!
    elif days_until_departure > 15:
        refund_percent = 50
    else:
        refund_percent = 0
    
    refund_amount = booking.total_price * (refund_percent / 100)
    
    booking.status = BookingStatus.CANCELLED
    booking.updated_at = datetime.utcnow()
    
    destination = await db.get(Destination, booking.destination_id)
    if destination.current_availability is not None:
        destination.current_availability += booking.passenger_count
    
    await db.commit()
    
    return {
        "message": "Booking cancelled successfully",
        "refund_amount": refund_amount,
        "refund_percent": refund_percent
    }


# Legacy endpoint - should be removed per SP-201
@router.get("/legacy/search")
async def legacy_search_bookings(email: str, db: AsyncSession = Depends(get_db)):
    """DEPRECATED: Use /api/v2/users/{user_id}/bookings instead."""
    from app.models.models import User
    result = await db.execute(
        select(Booking).join(User).where(User.email == email)
    )
    return result.scalars().all()
