import os
import sys
import logging
from dataclasses import dataclass, field
from datetime import date
.k
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

GRADUATION_DATE = date(2026, 6, 27)


@dataclass
class BotConfig:
    bot_token: str
    chat_id: str
    post_time: str
    timezone: str = "Africa/Addis_Ababa"  # UTC+3, change if needed
    graduation_date: date = field(default_factory=lambda: GRADUATION_DATE)


def load_config() -> BotConfig:
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")

    missing = []
    if not bot_token:
        missing.append("TELEGRAM_BOT_TOKEN")
    if not chat_id:
        missing.append("TELEGRAM_CHAT_ID")

    if missing:
        logger.error(
            "Missing required environment variable(s): %s. "
            "Set them in your environment or in a .env file.",
            ", ".join(missing),
        )
        sys.exit(1)

    raw_post_time = os.environ.get("POST_TIME", "")
    post_time = _parse_post_time(raw_post_time)
    timezone = os.environ.get("TIMEZONE", "Africa/Addis_Ababa")

    return BotConfig(bot_token=bot_token, chat_id=chat_id, post_time=post_time, timezone=timezone)


def _parse_post_time(value: str) -> str:
    """Validate HH:MM format; fall back to '09:00' if missing or malformed."""
    if not value:
        return "09:00"
    parts = value.split(":")
    if len(parts) == 2:
        try:
            hour, minute = int(parts[0]), int(parts[1])
            if 0 <= hour <= 23 and 0 <= minute <= 59:
                return f"{hour:02d}:{minute:02d}"
        except ValueError:
            pass
    logger.warning("POST_TIME '%s' is malformed; defaulting to '09:00'.", value)
    return "09:00"
