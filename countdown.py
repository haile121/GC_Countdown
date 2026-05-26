from datetime import date
from typing import Literal


def days_until_graduation(today: date, graduation_date: date) -> int:
    """Returns (graduation_date - today).days. Negative if past."""
    return (graduation_date - today).days


def graduation_status(
    today: date, graduation_date: date
) -> Literal["before", "today", "after"]:
    """Returns the relationship between today and graduation_date."""
    delta = (graduation_date - today).days
    if delta > 0:
        return "before"
    elif delta == 0:
        return "today"
    else:
        return "after"
