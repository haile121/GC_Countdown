import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st
from telegram.error import TelegramError

from sender import send_message


def _make_bot(fail_times: int):
    """Return a mock Bot that raises TelegramError for the first `fail_times` calls."""
    call_count = {"n": 0}

    async def _send(**kwargs):
        call_count["n"] += 1
        if call_count["n"] <= fail_times:
            raise TelegramError("network error")

    bot = MagicMock()
    bot.send_message = AsyncMock(side_effect=_send)
    return bot, call_count


@pytest.mark.asyncio
async def test_success_on_first_attempt():
    bot, counts = _make_bot(0)
    result = await send_message(bot, "123", "hello", retries=3, delay=0)
    assert result is True
    assert counts["n"] == 1


@pytest.mark.asyncio
async def test_success_on_second_attempt():
    bot, counts = _make_bot(1)
    result = await send_message(bot, "123", "hello", retries=3, delay=0)
    assert result is True
    assert counts["n"] == 2


@pytest.mark.asyncio
async def test_all_attempts_fail():
    bot, counts = _make_bot(10)
    result = await send_message(bot, "123", "hello", retries=3, delay=0)
    assert result is False
    assert counts["n"] == 3


@pytest.mark.asyncio
async def test_exactly_three_attempts_on_failure():
    bot, counts = _make_bot(100)
    await send_message(bot, "123", "hello", retries=3, delay=0)
    assert counts["n"] == 3


# ---------------------------------------------------------------------------
# Feature: telegram-graduation-countdown-bot, Property 5: Retry Behavior on Send Failure
# ---------------------------------------------------------------------------

@given(st.integers(min_value=1, max_value=10))
@settings(max_examples=100)
def test_retry_attempt_count(failures):
    """Property 5: Sender makes exactly min(failures, 3) attempts for any failure count."""
    bot, counts = _make_bot(failures)

    async def _run():
        return await send_message(bot, "123", "hello", retries=3, delay=0)

    asyncio.run(_run())
    expected_attempts = min(failures, 3)
    assert counts["n"] == expected_attempts
