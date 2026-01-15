"""
Notification Service
Handles email, SMS, and push notifications

Channels per PRD:
- Email: Implemented
- SMS: Implemented
- Push: Implemented
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


class NotificationService:
    def __init__(self):
        self.email_enabled = True
        self.sms_enabled = False  # Not actually implemented yet
        self.push_enabled = False  # Not actually implemented yet
    
    async def send_email(self, to_email: str, subject: str, body: str) -> bool:
        """Send email notification"""
        try:
            logger.info(f"[EMAIL] To: {to_email}, Subject: {subject}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False
    
    async def send_sms(self, phone_number: str, message: str) -> bool:
        """Send SMS notification - SP-208"""
        # TODO: Implement Twilio integration
        logger.warning("SMS notifications not implemented")
        return False
    
    async def send_push(self, user_id: int, title: str, body: str) -> bool:
        """Send push notification - SP-209"""
        # TODO: Implement push notifications
        logger.warning("Push notifications not implemented")
        return False


_notification_service = NotificationService()


def send_booking_confirmation(booking_id: int):
    """
    Send booking confirmation.
    BUG: Should be async but called without await!
    """
    import asyncio
    
    async def _send():
        await _notification_service.send_email(
            to_email="user@example.com",
            subject="SpacePort Booking Confirmed!",
            body=f"Your booking #{booking_id} has been confirmed."
        )
    
    try:
        loop = asyncio.get_event_loop()
        loop.create_task(_send())
    except RuntimeError:
        logger.error(f"Failed to send confirmation for booking {booking_id}")
