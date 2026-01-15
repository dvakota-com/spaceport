"""
Payments API Router
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
import uuid

from app.core.database import get_db

router = APIRouter()

SUPPORTED_METHODS = ["credit_card", "debit_card", "bank_transfer"]

@router.post("/")
async def process_payment(
    booking_id: int,
    amount: float,
    payment_method: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Process payment for booking.
    Supported methods: credit_card, debit_card, bank_transfer
    """
    if payment_method not in SUPPORTED_METHODS:
        raise HTTPException(status_code=400, detail="Unsupported payment method")
    
    transaction_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"
    
    return {
        "transaction_id": transaction_id,
        "amount": amount,
        "status": "completed"
    }
