import pytest
from logging import Logger
from unittest.mock import Mock, MagicMock

import praw.models  # type: ignore

from fineladybot.database import Database

mock_logger = Mock(spec=Logger)


@pytest.fixture
def reddit() -> praw.Reddit:
    reddit = MagicMock(spec=praw.Reddit)
    reddit.subreddit = praw.models.SubredditHelper(reddit, None)
    return reddit


@pytest.fixture
def subreddit(reddit) -> praw.models.Subreddit:
    return praw.models.Subreddit(reddit, "testsub")


@pytest.fixture(scope="session")
def db():
    database = Database("test_db", mock_logger, True)
    return database
