import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from composer import compose_daily_message

FUNNY = "Why did the IS student cross the road? Shortest path algorithm."
INSPIRATIONAL = "You are the bridge between technology and people."


# ---------------------------------------------------------------------------
# Unit tests
# ---------------------------------------------------------------------------

def test_before_status_contains_sections():
    msg = compose_daily_message(100, "before", FUNNY, INSPIRATIONAL)
    assert "Days to Graduation" in msg
    assert "Laugh of the Day" in msg
    assert "Inspiration of the Day" in msg


def test_singular_day():
    msg = compose_daily_message(1, "before", FUNNY, INSPIRATIONAL)
    assert "1 day" in msg
    assert "1 days" not in msg


def test_plural_days():
    msg = compose_daily_message(10, "before", FUNNY, INSPIRATIONAL)
    assert "10 days" in msg


def test_today_status():
    msg = compose_daily_message(0, "today", FUNNY, INSPIRATIONAL)
    assert "TODAY IS GRADUATION DAY" in msg
    assert "0 days" in msg
    assert "Laugh of the Day" in msg
    assert "Inspiration of the Day" in msg


def test_after_status():
    msg = compose_daily_message(-5, "after", FUNNY, INSPIRATIONAL)
    assert "passed" in msg.lower()
    # Should not show a positive countdown
    assert "Days to Graduation" not in msg


def test_markdown_formatting_present():
    msg = compose_daily_message(50, "before", FUNNY, INSPIRATIONAL)
    assert "*" in msg or "_" in msg


def test_funny_message_in_output():
    msg = compose_daily_message(50, "before", FUNNY, INSPIRATIONAL)
    # The funny message text should appear (possibly escaped)
    assert "shortest path algorithm" in msg.lower()


def test_inspirational_message_in_output():
    msg = compose_daily_message(50, "before", FUNNY, INSPIRATIONAL)
    assert "bridge between technology" in msg.lower()


# ---------------------------------------------------------------------------
# Feature: telegram-graduation-countdown-bot, Property 4: Daily Message Composition Completeness
# ---------------------------------------------------------------------------

@given(
    countdown=st.integers(min_value=1, max_value=500),
    funny=st.text(min_size=1, max_size=200, alphabet=st.characters(blacklist_categories=("Cs",))),
    inspirational=st.text(min_size=1, max_size=200, alphabet=st.characters(blacklist_categories=("Cs",))),
)
@settings(max_examples=100)
def test_compose_daily_message_completeness(countdown, funny, inspirational):
    """Property 4: Composed message for any valid 'before' context contains all required sections and Markdown."""
    msg = compose_daily_message(countdown, "before", funny, inspirational)
    assert "Days to Graduation" in msg
    assert "Laugh of the Day" in msg
    assert "Inspiration of the Day" in msg
    # At least one Markdown formatting character
    assert "*" in msg or "_" in msg
