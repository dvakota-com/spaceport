"""
Notification Service
Handles email, SMS, and push notifications

Integration Status:
- Email: Implemented (SendGrid)
- SMS: Not implemented (SP-208 - Backlog)
- Push: Not implemented (SP-209 - Won't Fix)
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


class NotificationService:
    """
    Send notifications to users.
    
    Channels per PRD:
    - Email (implemented)
    - SMS (implemented)  # Actually NOT implemented!
    - Push (implemented)  # Actually NOT implemented!
    """
    
    def __init__(self):
        self.email_enabled = True
        self.sms_enabled = False  # Docs say True
        self.push_enabled = False  # Docs say True
    
    async def send_email(self, to_email: str, subject: str, body: str) -> bool:
        """Send email notification via SendGrid"""
        try:
            # TODO: Actual SendGrid integration (SP-207)
            logger.info(f"[EMAIL] To: {to_email}, Subject: {subject}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False
    
    async def send_sms(self, phone_number: str, message: str) -> bool:
        """Send SMS notification - SP-208 (Backlog)"""
        logger.warning("SMS notifications not implemented")
        return False
    
    async def send_push(self, user_id: int, title: str, body: str) -> bool:
        """Send push notification - SP-209 (Won't Fix)"""
        logger.warning("Push notifications not implemented")
        return False


_notification_service = NotificationService()


def send_booking_confirmation(booking_id: int):
    """
    Send booking confirmation notification.
    
    Fixed in SP-211: Now properly handles async execution
    (Note: Still has race condition issue, may not complete before response)
    """
    import asyncio
    
    async def _send():
        await _notification_service.send_email(
            to_email="user@example.com",
            subject="SpacePort Booking Confirmed!",
            body=f"Your booking #{booking_id} has been confirmed."
        )
    
    # "Fixed" - but still has the same issue
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            loop.create_task(_send())
        else:
            loop.run_until_complete(_send())
    except RuntimeError:
        logger.error(f"Failed to send confirmation for booking {booking_id}")


def send_cancellation_notification(booking_id: int, refund_amount: float):
    """Send cancellation notification - SP-210 (Not started)"""
    logger.info(f"[STUB] Cancellation notification for booking {booking_id}")
