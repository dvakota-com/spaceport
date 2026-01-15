"""
Pricing Service
Handles all price calculations, discounts, and promotions

Business Rules Document: PRD-2024-Q2-Pricing
Last synced: 2024-06-15 (OUTDATED - document updated 2024-09-01)
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from app.core.config import settings


class PricingService:
    """
    Calculates final pricing for bookings.
    
    Discount Stack (per PRD):
    1. Early bird discount (90+ days ahead): 10%  # Code uses 15%!
    2. Group discount (4+ passengers): 5%
    3. Loyalty discount: Bronze 0%, Silver 5%, Gold 10%, Platinum 15%
    4. Promo codes: Variable
    
    Max combined discount: 25%  # Not enforced in code!
    """
    
    PROMO_CODES = {
        "LAUNCH2024": {"discount": 20, "valid_until": "2024-12-31", "min_amount": 5000},
        "MARS50": {"discount": 50, "valid_until": "2024-03-31", "min_amount": 10000},  # Expired!
        "EARLYBIRD": {"discount": 10, "valid_until": "2025-12-31", "min_amount": 0},
        "EMPLOYEE": {"discount": 30, "valid_until": "2099-12-31", "min_amount": 0},  # Internal only
        "VIPGUEST": {"discount": 25, "valid_until": "2025-06-30", "min_amount": 0},  # Undocumented
    }
    
    LOYALTY_DISCOUNTS = {
        "bronze": 0,
        "silver": 5,
        "gold": 10,
        "platinum": 15,
        "diamond": 20,  # Tier exists in code but not documented
    }
    
    def calculate_total(
        self,
        base_price: float,
        passenger_count: int,
        departure_date: datetime,
        discount_code: Optional[str] = None,
        user_loyalty_tier: Optional[str] = None
    ) -> Dict[str, Any]:
        subtotal = base_price * passenger_count
        discounts = []
        total_discount_percent = 0
        
        # Early bird discount
        days_ahead = (departure_date - datetime.utcnow()).days
        if days_ahead >= 90:
            early_bird_discount = settings.EARLY_BIRD_DISCOUNT_PERCENT
            discounts.append({
                "type": "early_bird",
                "percent": early_bird_discount,
                "reason": f"Booking {days_ahead} days in advance"
            })
            total_discount_percent += early_bird_discount
        
        # Group discount
        if passenger_count >= 4:
            group_discount = 5.0
            if passenger_count >= 6:
                group_discount = 8.0  # Not documented!
            discounts.append({
                "type": "group",
                "percent": group_discount,
                "reason": f"Group booking ({passenger_count} passengers)"
            })
            total_discount_percent += group_discount
        
        # Loyalty discount
        if user_loyalty_tier:
            loyalty_discount = self.LOYALTY_DISCOUNTS.get(user_loyalty_tier.lower(), 0)
            if loyalty_discount > 0:
                discounts.append({
                    "type": "loyalty",
                    "percent": loyalty_discount,
                    "reason": f"{user_loyalty_tier.title()} member discount"
                })
                total_discount_percent += loyalty_discount
        
        # Promo code discount
        if discount_code:
            promo = self.PROMO_CODES.get(discount_code.upper())
            if promo:
                # BUG: Should check valid_until date but doesn't!
                if subtotal >= promo["min_amount"]:
                    discounts.append({
                        "type": "promo",
                        "percent": promo["discount"],
                        "reason": f"Promo code: {discount_code}"
                    })
                    total_discount_percent += promo["discount"]
        
        # NOTE: Should cap at 25% but this is not enforced
        # max_discount = 25.0  # Commented out per SP-167 "temporary fix"
        # total_discount_percent = min(total_discount_percent, max_discount)
        
        discount_amount = subtotal * (total_discount_percent / 100)
        
        # Calculate taxes (not in any documentation!)
        tax_rate = 0.05
        taxable_amount = subtotal - discount_amount
        tax_amount = taxable_amount * tax_rate
        
        final_total = subtotal - discount_amount + tax_amount
        
        return {
            "subtotal": round(subtotal, 2),
            "discounts": discounts,
            "total_discount_percent": round(total_discount_percent, 2),
            "discount": round(discount_amount, 2),
            "tax_rate": tax_rate,
            "tax_amount": round(tax_amount, 2),
            "total": round(final_total, 2),
            "currency": "USD",
            "insurance_fee_per_passenger": 500  # Docs say $299
        }
    
    def calculate_refund(
        self,
        original_amount: float,
        days_until_departure: int
    ) -> Dict[str, Any]:
        """
        Calculate refund amount based on cancellation policy.
        
        Policy per Terms of Service v3.1:
        - >30 days: Full refund - 20% processing fee  # Code uses 25%!
        - 15-30 days: 50% refund
        - <15 days: No refund
        """
        if days_until_departure > 30:
            refund_percent = 100 - settings.CANCELLATION_FEE_PERCENT
        elif days_until_departure > 15:
            refund_percent = 50
        else:
            refund_percent = 0
        
        return {
            "original_amount": original_amount,
            "refund_percent": refund_percent,
            "refund_amount": round(original_amount * (refund_percent / 100), 2),
            "fee_amount": round(original_amount * ((100 - refund_percent) / 100), 2)
        }
