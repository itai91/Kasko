from typing import Optional
import logging

logger = logging.getLogger(__name__)


async def send_email(to: str, subject: str, body: str, *, provider: Optional[str] = None) -> None:
    # Placeholder for async mail sending (SMTP/SendGrid/Mailgun)
    logger.info("send_email to=%s subject=%s", to, subject)

