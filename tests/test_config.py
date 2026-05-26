import os
import sys
from unittest.mock import patch

import pytest

from config import _parse_post_time, load_config


def test_parse_post_time_valid():
    assert _parse_post_time("09:00") == "09:00"
    assert _parse_post_time("23:59") == "23:59"
    assert _parse_post_time("00:00") == "00:00"


def test_parse_post_time_empty_defaults():
    assert _parse_post_time("") == "09:00"


def test_parse_post_time_malformed_defaults():
    assert _parse_post_time("9am") == "09:00"
    assert _parse_post_time("25:00") == "09:00"
    assert _parse_post_time("12:99") == "09:00"


def test_load_config_missing_token_exits():
    env = {"TELEGRAM_CHAT_ID": "-100", "TELEGRAM_BOT_TOKEN": ""}
    with patch.dict(os.environ, env, clear=True):
        with pytest.raises(SystemExit) as exc_info:
            load_config()
    assert exc_info.value.code != 0


def test_load_config_missing_chat_id_exits():
    env = {"TELEGRAM_BOT_TOKEN": "abc123", "TELEGRAM_CHAT_ID": ""}
    with patch.dict(os.environ, env, clear=True):
        with pytest.raises(SystemExit) as exc_info:
            load_config()
    assert exc_info.value.code != 0


def test_load_config_defaults_post_time():
    env = {"TELEGRAM_BOT_TOKEN": "abc123", "TELEGRAM_CHAT_ID": "-100"}
    with patch.dict(os.environ, env, clear=True):
        config = load_config()
    assert config.post_time == "09:00"


def test_load_config_custom_post_time():
    env = {
        "TELEGRAM_BOT_TOKEN": "abc123",
        "TELEGRAM_CHAT_ID": "-100",
        "POST_TIME": "14:30",
    }
    with patch.dict(os.environ, env, clear=True):
        config = load_config()
    assert config.post_time == "14:30"
