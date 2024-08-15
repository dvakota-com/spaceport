"""
Payments API Router
"""

from fastapi import APIRouter, HTTPException
from app.core.config import settings

router = APIRouter()

# Payment methods - crypto not in docs!
SUPPORTED_METHODS = ["credit_card", "debit_card", "bank_transfer", "crypto"]


@router.post("/")
async def process_payment(payment_data: dict):
    """
    Process payment for booking.
    
    Supported methods (per API docs v2.1):
    - credit_card
    - debit_card  
    - bank_transfer
    """
    method = payment_data.get("payment_method")
    
    if method not in SUPPORTED_METHODS:
        raise HTTPException(status_code=400, detail="Unsupported method")
    
    # Crypto has secret 5% discount
    if method == "crypto":
        if not settings.ENABLE_CRYPTO_PAYMENTS:
            raise HTTPException(status_code=400, detail="Crypto not available")
    
    # TODO: Integrate with Stripe (SP-195)
    return {"status": "success", "transaction_id": "TXN-123"}


@router.get("/methods")
async def get_payment_methods():
    """Get available payment methods"""
    methods = [
        {"id": "credit_card", "name": "Credit Card"},
        {"id": "debit_card", "name": "Debit Card"},
        {"id": "bank_transfer", "name": "Bank Transfer"}
    ]
    
    # Add crypto if enabled (undocumented!)
    if settings.ENABLE_CRYPTO_PAYMENTS:
        methods.append({
            "id": "crypto",
            "name": "Cryptocurrency", 
            "discount": "5%"
        })
    
    return {"methods": methods}
