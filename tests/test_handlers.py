import tempfile
from datetime import date
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from telegram.constants import ChatMemberStatus

from config import BotConfig
from messages import MessageCycler


def _make_update(user_id: int = 1, chat_id: int = -100):
    update = MagicMock()
    update.effective_user.id = user_id
    update.effective_chat.id = chat_id
    update.message.reply_text = AsyncMock()
    return update


def _make_context(config: BotConfig, tmp_path, member_status: str):
    context = MagicMock()
    context.bot.get_chat_member = AsyncMock(
        return_value=MagicMock(status=member_status)
    )
    context.bot.send_message = AsyncMock()

    funny_cycler = MessageCycler(
        ["funny1", "funny2"], state_key="funny", state_file=str(tmp_path / "state.json")
    )
    inspirational_cycler = MessageCycler(
        ["insp1", "insp2"], state_key="inspirational", state_file=str(tmp_path / "state.json")
    )

    context.bot_data = {
        "config": config,
        "funny_cycler": funny_cycler,
        "inspirational_cycler": inspirational_cycler,
    }
    return context


def _make_config():
    return BotConfig(
        bot_token="test_token",
        chat_id="-100",
        post_time="09:00",
        graduation_date=date(2026, 6, 22),
    )


@pytest.mark.asyncio
async def test_today_handler_admin_sends_message(tmp_path):
    from handlers import today_handler

    config = _make_config()
    update = _make_update()
    context = _make_context(config, tmp_path, ChatMemberStatus.ADMINISTRATOR)

    await today_handler(update, context)

    context.bot.send_message.assert_called_once()


@pytest.mark.asyncio
async def test_today_handler_non_admin_rejected(tmp_path):
    from handlers import today_handler

    config = _make_config()
    update = _make_update()
    context = _make_context(config, tmp_path, ChatMemberStatus.MEMBER)

    await today_handler(update, context)

    update.message.reply_text.assert_called_once()
    call_args = update.message.reply_text.call_args[0][0]
    assert "restricted" in call_args.lower()
    context.bot.send_message.assert_not_called()


@pytest.mark.asyncio
async def test_start_handler_includes_posting_time(tmp_path):
    from handlers import start_handler

    config = _make_config()
    update = _make_update()
    context = _make_context(config, tmp_path, ChatMemberStatus.MEMBER)

    await start_handler(update, context)

    update.message.reply_text.assert_called_once()
    reply_text = update.message.reply_text.call_args[0][0]
    assert "09:00" in reply_text


@pytest.mark.asyncio
async def test_start_handler_mentions_graduation_date(tmp_path):
    from handlers import start_handler

    config = _make_config()
    update = _make_update()
    context = _make_context(config, tmp_path, ChatMemberStatus.MEMBER)

    await start_handler(update, context)

    reply_text = update.message.reply_text.call_args[0][0]
    assert "June 22, 2026" in reply_text
