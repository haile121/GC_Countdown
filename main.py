import logging
from datetime import date, timezone, timedelta

from telegram.ext import Application, CommandHandler

from composer import compose_daily_message
from config import load_config
from countdown import days_until_graduation, graduation_status
from handlers import start_handler, today_handler
from messages import FUNNY_MESSAGES, INSPIRATIONAL_MESSAGES, MessageCycler
from scheduler import setup_scheduler
from sender import send_message

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def daily_job(context) -> None:
    """Job function called by the scheduler each day."""
    config = context.bot_data["config"]
    funny_cycler: MessageCycler = context.bot_data["funny_cycler"]
    inspirational_cycler: MessageCycler = context.bot_data["inspirational_cycler"]

    today = date.today()
    countdown = days_until_graduation(today, config.graduation_date)
    status = graduation_status(today, config.graduation_date)

    funny = funny_cycler.next()
    inspirational = inspirational_cycler.next()

    text = compose_daily_message(countdown, status, funny, inspirational)
    await send_message(context.bot, config.chat_id, text)


def main() -> None:
    import os
    from telegram.ext import JobQueue
    config = load_config()

    builder = Application.builder().token(config.bot_token)

    proxy_url = os.environ.get("PROXY_URL", "")
    if proxy_url:
        from telegram.request import HTTPXRequest
        builder = builder.request(HTTPXRequest(proxy=proxy_url))
        logger.info("Using proxy: %s", proxy_url)

    app = builder.build()

    if app.job_queue is None:
        logger.error("JobQueue is not available. Make sure 'python-telegram-bot[job-queue]' is installed.")
        raise RuntimeError("JobQueue unavailable")

    # Store shared state in bot_data
    app.bot_data["config"] = config
    app.bot_data["funny_cycler"] = MessageCycler(
        FUNNY_MESSAGES, state_key="funny_index"
    )
    app.bot_data["inspirational_cycler"] = MessageCycler(
        INSPIRATIONAL_MESSAGES, state_key="inspirational_index"
    )

    # Register command handlers
    app.add_handler(CommandHandler("today", today_handler))
    app.add_handler(CommandHandler("start", start_handler))

    # Set up daily scheduler
    setup_scheduler(app, config, daily_job)

    logger.info("Bot starting. Daily message scheduled at %s.", config.post_time)
    app.run_polling()


if __name__ == "__main__":
    main()
