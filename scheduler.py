import logging
from datetime import time
from typing import Callable
from zoneinfo import ZoneInfo

from telegram.ext import Application

from config import BotConfig

logger = logging.getLogger(__name__)


def setup_scheduler(app: Application, config: BotConfig, job_fn: Callable) -> None:
    """Register a daily cron job using python-telegram-bot's built-in JobQueue."""
    hour, minute = map(int, config.post_time.split(":"))
    # Use the configured timezone so POST_TIME is local time, not UTC
    tz = ZoneInfo(config.timezone)
    post_time = time(hour=hour, minute=minute, tzinfo=tz)

    app.job_queue.run_daily(
        job_fn,
        time=post_time,
        name="daily_countdown",
    )
    logger.info("Scheduled daily message at %s (%s).", config.post_time, config.timezone)
