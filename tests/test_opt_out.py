from datetime import datetime
from typing import Any
from unittest.mock import MagicMock
from urllib.parse import quote_plus

import pytest
from praw.models import Message, Subreddit, User
from praw import Reddit

from fineladybot.database import Database
from fineladybot.finelady import parse_sub_opt_out


@pytest.mark.parametrize(
    "user,date",
    [
        ("tim", datetime(2022, 1, 1)),
    ],
)
def test_user_opt_out(user, date, db: Database):
    db.add_opt_out_user(user, date)
    opted_out_users = db.query_users()
    assert opted_out_users[0] == user


def mock_moderator_method_factory(list_of_mods: list[str]) -> callable:
    def mock_moderator_method(self) -> list[str]:
        return list_of_mods

    return mock_moderator_method


@pytest.mark.parametrize(
    "author, mods, expected",
    [
        ("anon", ["mod1"], False),  # author is not mod
        ("mod1", ["mod1"], True),  # author is mod
    ],
)
def test_sub_opt_out(
    author: str,
    mods: list[str],
    expected: list[str],
    monkeypatch: Any,
    reddit: Reddit,
    subreddit: Subreddit,
    db: Database,
):
    mock_moderator_method = mock_moderator_method_factory(mods)
    monkeypatch.setattr(Subreddit, "moderator", mock_moderator_method)
    msg = MagicMock(spec=Message)
    user = MagicMock(spec=User)
    msg.created_utc = datetime(2022, 1, 1).timestamp()
    msg.body = f"Please do not post anything further to /r/{subreddit}"
    msg.author = user
    msg.author.name = author
    opted_out_subs = []
    parse_sub_opt_out(msg, reddit, db)
    opted_out_subs = db.query_subs()
    result = opted_out_subs == [subreddit.display_name]
    assert result == expected
