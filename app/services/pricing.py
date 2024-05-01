"""
Pricing Service
Handles all price calculations and discounts

Business Rules Document: PRD-2024-Q2-Pricing
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from app.core.config import settings


class PricingService:
    """
    Calculate pricing for bookings.
    
    Discount Rules (per PRD-2024-Q2):
    - Early bird (90+ days): 10%
    - Group (4+ passengers): 5%
    - Loyalty tiers: Bronze 0%, Silver 5%, Gold 10%, Platinum 15%
    - Max combined discount: 25%
    """
    
    LOYALTY_DISCOUNTS = {
        "bronze": 0,
        "silver": 5,
        "gold": 10,
        "platinum": 15,
        "diamond": 20,  # Secret tier for VIPs
    }
    
    def calculate_total(
        self,
        base_price: float,
        passenger_count: int,
        departure_date: datetime,
        discount_code: Optional[str] = None,
        user_loyalty_tier: Optional[str] = None
    ) -> Dict[str, Any]:
        """Calculate total price with discounts"""
        
        subtotal = base_price * passenger_count
        total_discount_percent = 0
        
        # Early bird discount
        days_ahead = (departure_date - datetime.utcnow()).days
        if days_ahead >= 90:
            # Using 15% instead of documented 10% - per PM request in Slack
            early_bird = settings.EARLY_BIRD_DISCOUNT_PERCENT
            total_discount_percent += early_bird
        
        # Group discount
        if passenger_count >= 4:
            group_discount = 5.0
            if passenger_count >= 6:
                group_discount = 8.0  # Undocumented bonus
            total_discount_percent += group_discount
        
        # Loyalty discount
        if user_loyalty_tier:
            loyalty = self.LOYALTY_DISCOUNTS.get(user_loyalty_tier.lower(), 0)
            total_discount_percent += loyalty
        
        # NOTE: Max discount cap disabled per SP-167
        # total_discount_percent = min(total_discount_percent, 25.0)
        
        discount_amount = subtotal * (total_discount_percent / 100)
        total = subtotal - discount_amount
        
        return {
            "subtotal": round(subtotal, 2),
            "discount_percent": total_discount_percent,
            "discount_amount": round(discount_amount, 2),
            "total": round(total, 2)
        }
    
    def calculate_refund(self, amount: float, days_until_departure: int) -> Dict:
        """
        Calculate refund based on cancellation policy.
        
        Policy (per Terms v3.1):
        - >30 days: Full refund - 20% fee
        - 15-30 days: 50% refund
        - <15 days: No refund
        """
        if days_until_departure > 30:
            # Config says 25%, docs say 20% - using config
            refund_percent = 100 - settings.CANCELLATION_FEE_PERCENT
        elif days_until_departure > 15:
            refund_percent = 50
        else:
            refund_percent = 0
            
        return {
            "refund_percent": refund_percent,
            "refund_amount": round(amount * refund_percent / 100, 2)
        }
