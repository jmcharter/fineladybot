import pytest
import praw.models


@pytest.fixture
def subreddit() -> praw.models.Subreddit:
    return praw.models.Subreddit(None, "testsub")
