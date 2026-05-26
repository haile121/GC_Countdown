import re
from datetime import date
from typing import Literal

# Characters that must be escaped in Telegram MarkdownV2
_ESCAPE_CHARS = r"\_*[]()~`>#+-=|{}.!"

_GRADUATION_DATE = date(2026, 6, 27)
_JOURNEY_START = date(2026, 1, 1)  # start of the year
_TOTAL_DAYS = (_GRADUATION_DATE - _JOURNEY_START).days  # Jan 1 → Jun 27
_BAR_LENGTH = 20


def _escape(text: str) -> str:
    """Escape special MarkdownV2 characters in plain text."""
    return re.sub(r"([" + re.escape(_ESCAPE_CHARS) + r"])", r"\\\1", text)


def _progress_bar(countdown: int) -> str:
    """
    Build a visual progress bar showing how far through the journey we are.
    days_elapsed = _TOTAL_DAYS - countdown
    """
    days_elapsed = max(0, _TOTAL_DAYS - countdown)
    filled = round((days_elapsed / _TOTAL_DAYS) * _BAR_LENGTH)
    filled = max(0, min(filled, _BAR_LENGTH))
    empty = _BAR_LENGTH - filled
    bar = "█" * filled + "░" * empty
    percent = round((days_elapsed / _TOTAL_DAYS) * 100)
    return f"`{bar}` {percent}%"


def compose_daily_message(
    countdown: int,
    status: Literal["before", "today", "after"],
    funny: str,
    inspirational: str,
) -> str:
    """Return a Telegram MarkdownV2-formatted daily message string."""

    if status == "after":
        return (
            "🎓 *Graduation has already passed\\!*\n\n"
            "Hope you're enjoying life as an IS graduate\\. 🚀"
        )

    if status == "today":
        bar_line = _progress_bar(0)
        header = (
            "🎓 *TODAY IS GRADUATION DAY\\!* 🎓\n\n"
            f"📊 *Progress:* {bar_line}\n"
            "*Days to Graduation:* 0 days\n"
        )
        celebration = (
            "\n\n🎉 *Congratulations, IS graduates\\!* "
            "You made it\\! Time to celebrate\\! 🥳"
        )
    else:
        day_word = "day" if countdown == 1 else "days"
        bar_line = _progress_bar(countdown)
        header = (
            f"📈 *Progress:* {bar_line}\n"
            f"🎓 *{countdown} {day_word} left until Graduation\\!*\n"
        )
        celebration = ""

    funny_section = (
        "\n😁 *Laugh of the Day:*\n"
        f"_{_escape(funny)}_"
    )

    inspirational_section = (
        "\n\n🔥 *Inspiration of the Day:*\n"
        f"_{_escape(inspirational)}_"
    )

    return header + funny_section + inspirational_section + celebration
