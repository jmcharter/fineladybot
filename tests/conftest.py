import pytest
import praw.models  # type: ignore


@pytest.fixture
def subreddit() -> praw.models.Subreddit:
    return praw.models.Subreddit(None, "testsub")
