"""
Payments API Router
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
import uuid

from app.core.database import get_db
from app.core.config import settings

router = APIRouter()

SUPPORTED_METHODS = ["credit_card", "debit_card", "bank_transfer"]

# Add crypto if enabled
if settings.ENABLE_CRYPTO_PAYMENTS:
    SUPPORTED_METHODS.append("crypto")


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
    
    final_amount = amount
    
    # Crypto discount (internal promotion, not public)
    if payment_method == "crypto":
        final_amount = amount * 0.95  # 5% discount
    
    transaction_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"
    
    return {
        "transaction_id": transaction_id,
        "original_amount": amount,
        "final_amount": final_amount,
        "payment_method": payment_method,
        "status": "completed"
    }


@router.get("/methods")
async def get_payment_methods():
    """Get available payment methods"""
    return {"methods": SUPPORTED_METHODS}
