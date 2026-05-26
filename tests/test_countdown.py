from datetime import date

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from countdown import days_until_graduation, graduation_status

GRADUATION_DATE = date(2026, 6, 22)


# ---------------------------------------------------------------------------
# Unit tests
# ---------------------------------------------------------------------------

def test_days_before_graduation():
    today = date(2026, 6, 21)
    assert days_until_graduation(today, GRADUATION_DATE) == 1


def test_days_on_graduation():
    assert days_until_graduation(GRADUATION_DATE, GRADUATION_DATE) == 0


def test_days_after_graduation():
    today = date(2026, 6, 23)
    assert days_until_graduation(today, GRADUATION_DATE) == -1


def test_status_before():
    assert graduation_status(date(2025, 1, 1), GRADUATION_DATE) == "before"


def test_status_today():
    assert graduation_status(GRADUATION_DATE, GRADUATION_DATE) == "today"


def test_status_after():
    assert graduation_status(date(2026, 6, 23), GRADUATION_DATE) == "after"


# ---------------------------------------------------------------------------
# Feature: telegram-graduation-countdown-bot, Property 1: Countdown Calculation Correctness
# ---------------------------------------------------------------------------

@given(st.dates(min_value=date(2024, 1, 1), max_value=date(2026, 6, 21)))
@settings(max_examples=100)
def test_countdown_calculation_correctness(today):
    """Property 1: days_until_graduation returns (grad - today).days for any pre-graduation date."""
    result = days_until_graduation(today, GRADUATION_DATE)
    expected = (GRADUATION_DATE - today).days
    assert result == expected
    assert result > 0


# ---------------------------------------------------------------------------
# Feature: telegram-graduation-countdown-bot, Property 2: Post-Graduation Message
# ---------------------------------------------------------------------------

@given(st.dates(min_value=date(2026, 6, 23), max_value=date(2030, 12, 31)))
@settings(max_examples=100)
def test_post_graduation_status(today):
    """Property 2: Any date after graduation must return status 'after' and negative days."""
    status = graduation_status(today, GRADUATION_DATE)
    days = days_until_graduation(today, GRADUATION_DATE)
    assert status == "after"
    assert days < 0
