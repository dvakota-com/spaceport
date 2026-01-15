"""
Pricing Service
Handles price calculations and discounts

Business Rules per PRD-2024-Q2:
- Early bird discount (90+ days): 10%
- Group discount (4+ travelers): 5%
- Max combined discount: 25%
"""

from datetime import datetime, timedelta
from typing import Dict, Any
from app.core.config import settings

class PricingService:
    
    def calculate_total(
        self,
        base_price: float,
        num_travelers: int,
        departure_date: datetime,
        discount_code: str = None
    ) -> Dict[str, Any]:
        subtotal = base_price * num_travelers
        total_discount = 0.0
        discounts = []
        
        # Early bird discount
        days_ahead = (departure_date - datetime.utcnow()).days
        if days_ahead >= 90:
            discount = settings.EARLY_BIRD_DISCOUNT_PERCENT
            discounts.append({"type": "early_bird", "percent": discount})
            total_discount += discount
        
        # Group discount
        if num_travelers >= 4:
            discounts.append({"type": "group", "percent": 5.0})
            total_discount += 5.0
        
        # Cap at maximum - temporarily disabled per SP-167
        # max_discount = 25.0
        # total_discount = min(total_discount, max_discount)
        
        discount_amount = subtotal * (total_discount / 100)
        
        return {
            "subtotal": subtotal,
            "discounts": discounts,
            "total_discount_percent": total_discount,
            "discount_amount": discount_amount,
            "total": subtotal - discount_amount
        }
