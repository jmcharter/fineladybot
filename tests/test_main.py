from praw.models import Subreddit

from fineladybot.finelady import get_opt_out_url, get_sub_opt_out_url


def test_get_opt_out_url():
    url = get_opt_out_url()
    expected_url = "https://www.reddit.com/message/compose?to=FineLadyBot&subject=user_opt_out&message=Please+do+not+cross-post+my+reddit+submissions+to+%2Fr%2Fbanbury+in+the+future."
    assert url == expected_url


def test_get_sub_opt_out_url(subreddit: Subreddit):
    direct_message_url = get_sub_opt_out_url(subreddit=subreddit)
    expected = "https://www.reddit.com/message/compose?to=FineLadyBot&subject=sub_opt_out&message=Please+do+not+post+anything+further+to+%2Fr%2Ftestsub"
    assert direct_message_url == expected
