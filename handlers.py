import logging
from datetime import date

from telegram import Update
from telegram.constants import ChatMemberStatus
from telegram.ext import ContextTypes

from composer import compose_daily_message
from config import BotConfig
from countdown import days_until_graduation, graduation_status
from messages import FUNNY_MESSAGES, INSPIRATIONAL_MESSAGES, MessageCycler
from sender import send_message

logger = logging.getLogger(__name__)

_ADMIN_STATUSES = {ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER}


async def _is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    member = await context.bot.get_chat_member(chat_id, user_id)
    return member.status in _ADMIN_STATUSES


async def today_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /today — admin only. Posts the daily message immediately."""
    if not await _is_admin(update, context):
        await update.message.reply_text(
            "This command is restricted to group admins."
        )
        return

    config: BotConfig = context.bot_data["config"]
    funny_cycler: MessageCycler = context.bot_data["funny_cycler"]
    inspirational_cycler: MessageCycler = context.bot_data["inspirational_cycler"]

    today = date.today()
    countdown = days_until_graduation(today, config.graduation_date)
    status = graduation_status(today, config.graduation_date)

    funny = funny_cycler.next()
    inspirational = inspirational_cycler.next()

    text = compose_daily_message(countdown, status, funny, inspirational)
    await send_message(context.bot, config.chat_id, text)


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start — reply with bot description and configured posting time."""
    config: BotConfig = context.bot_data["config"]
    await update.message.reply_text(
        f"👋 Hi! I'm the IS Graduation Countdown Bot.\n\n"
        f"Every day at {config.post_time} I post a countdown to graduation "
        f"(June 27, 2026) along with a funny IS-themed message and an "
        f"inspirational quote.\n\n"
        f"Group admins can also use /today to trigger the message manually."
    )
