import json
import tempfile
from pathlib import Path

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from messages import MessageCycler, FUNNY_MESSAGES, INSPIRATIONAL_MESSAGES


# ---------------------------------------------------------------------------
# Unit tests
# ---------------------------------------------------------------------------

def _make_cycler(messages, tmp_path, key="test"):
    state_file = str(tmp_path / "cycle_state.json")
    return MessageCycler(messages, state_key=key, state_file=state_file)


def test_cycler_returns_first_message(tmp_path):
    msgs = ["a", "b", "c"]
    cycler = _make_cycler(msgs, tmp_path)
    assert cycler.next() == "a"


def test_cycler_wraps_around(tmp_path):
    msgs = ["a", "b"]
    cycler = _make_cycler(msgs, tmp_path)
    cycler.next()  # a
    cycler.next()  # b
    assert cycler.next() == "a"  # wraps


def test_cycler_persists_index(tmp_path):
    msgs = ["a", "b", "c"]
    state_file = str(tmp_path / "cycle_state.json")
    c1 = MessageCycler(msgs, state_key="k", state_file=state_file)
    c1.next()  # a -> index becomes 1
    # New instance reads persisted index
    c2 = MessageCycler(msgs, state_key="k", state_file=state_file)
    assert c2.next() == "b"


def test_cycler_corrupt_state_resets(tmp_path):
    state_file = tmp_path / "cycle_state.json"
    state_file.write_text("not valid json{{")
    cycler = MessageCycler(["x", "y"], state_key="k", state_file=str(state_file))
    assert cycler.next() == "x"


def test_cycler_empty_raises():
    with pytest.raises(ValueError):
        MessageCycler([], state_key="k", state_file="/tmp/dummy.json")


def test_funny_messages_count():
    assert len(FUNNY_MESSAGES) >= 30


def test_inspirational_messages_count():
    assert len(INSPIRATIONAL_MESSAGES) >= 30


# ---------------------------------------------------------------------------
# Feature: telegram-graduation-countdown-bot, Property 3: Message Cycle Exhaustion
# ---------------------------------------------------------------------------

@given(st.lists(st.text(min_size=1), min_size=1, max_size=50))
@settings(max_examples=100)
def test_message_cycle_exhaustion(messages):
    """Property 3: Cycling through N messages returns each exactly once before wrapping."""
    with tempfile.TemporaryDirectory() as tmp:
        from pathlib import Path
        state_file = str(Path(tmp) / "cycle_state.json")
        cycler = MessageCycler(messages, state_key="test", state_file=state_file)
        seen = [cycler.next() for _ in range(len(messages))]
        assert sorted(seen) == sorted(messages)
        # After full cycle, next call wraps back to first message
        assert cycler.next() == messages[0]
