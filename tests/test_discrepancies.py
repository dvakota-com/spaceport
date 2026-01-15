"""
SpacePort API Tests

Note: These tests document expected vs actual behavior.
Many will fail due to code/documentation mismatches.
"""

import pytest
from datetime import datetime, timedelta


class TestPricingDiscrepancies:
    """Tests documenting pricing discrepancies"""
    
    def test_early_bird_discount_per_docs(self):
        """
        Per PRD-2024-Q2: Early bird discount should be 10%
        ACTUAL: Code uses 15% (config.EARLY_BIRD_DISCOUNT_PERCENT)
        """
        from app.core.config import settings
        expected = 10.0  # Per documentation
        actual = settings.EARLY_BIRD_DISCOUNT_PERCENT
        assert actual == expected, f"Expected {expected}%, got {actual}%"
    
    def test_max_passengers_per_docs(self):
        """
        Per PRD: Maximum 6 passengers per booking
        ACTUAL: Config allows 8 passengers
        """
        from app.core.config import settings
        expected = 6
        actual = settings.MAX_PASSENGERS_PER_BOOKING
        assert actual == expected, f"Expected {expected}, got {actual}"
    
    def test_cancellation_fee_per_docs(self):
        """
        Per Terms v3.1: Cancellation fee is 20%
        ACTUAL: Config uses 25%
        """
        from app.core.config import settings
        expected = 20.0
        actual = settings.CANCELLATION_FEE_PERCENT
        assert actual == expected, f"Expected {expected}%, got {actual}%"


class TestSecurityDiscrepancies:
    """Tests documenting security issues"""
    
    def test_token_expiration_per_docs(self):
        """
        Per API docs: Tokens expire after 60 minutes
        ACTUAL: Config sets 30 minutes
        """
        from app.core.config import settings
        expected = 60
        actual = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        assert actual == expected, f"Expected {expected} min, got {actual} min"
    
    def test_bcrypt_implementation(self):
        """
        SP-190 marked as Done: Password hashing with bcrypt
        ACTUAL: Still using MD5!
        """
        from app.routers.users import hash_password
        test_hash = hash_password("test123")
        # MD5 produces 32 char hex string, bcrypt starts with $2b$
        is_bcrypt = test_hash.startswith("$2b$")
        assert is_bcrypt, "Password hashing should use bcrypt, not MD5"


class TestFeatureFlagDiscrepancies:
    """Tests documenting feature flag issues"""
    
    def test_waitlist_feature_enabled(self):
        """
        SP-156 marked as Done: Waitlist feature
        ACTUAL: Feature flag is disabled!
        """
        from app.core.config import settings
        assert settings.ENABLE_WAITLIST == True, "Waitlist should be enabled per SP-156"
    
    def test_crypto_payments_documented(self):
        """
        Documentation: Crypto payments not available
        ACTUAL: Feature is enabled and working!
        """
        from app.core.config import settings
        # Per docs, this should be False
        # But it's actually True (undocumented feature)
        assert settings.ENABLE_CRYPTO_PAYMENTS == False, "Crypto should not be enabled per docs"
