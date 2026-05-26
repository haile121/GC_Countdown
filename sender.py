import asyncio
import logging
from datetime import datetime, timezone

from telegram import Bot
from telegram.error import TelegramError

logger = logging.getLogger(__name__)


async def send_message(
    bot: Bot,
    chat_id: str,
    text: str,
    retries: int = 3,
    delay: int = 60,
) -> bool:
    """
    Attempt to send a Telegram message up to `retries` times.
    Waits `delay` seconds between attempts.
    Returns True on success, False if all attempts fail.
    """
    for attempt in range(1, retries + 1):
        try:
            await bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode="MarkdownV2",
            )
            logger.info("Message sent successfully on attempt %d.", attempt)
            return True
        except TelegramError as exc:
            logger.warning(
                "Send attempt %d/%d failed: %s", attempt, retries, exc
            )
            if attempt < retries:
                await asyncio.sleep(delay)

    timestamp = datetime.now(tz=timezone.utc).isoformat()
    logger.error(
        "[%s] All %d send attempts failed. Message not delivered.", timestamp, retries
    )
    return False
