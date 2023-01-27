# !/usr/bin/python3
from typing import Iterator, Union
from dotenv import load_dotenv
from datetime import datetime
from urllib.parse import quote_plus

import praw, logging, pathlib, regex
from praw.models import Submission, Message, Subreddit
from praw.models.reddit.subreddit import SubredditStream

from fineladybot.database import Database
from fineladybot.interfaces.reddit import PrawConfig, ParsedSubmission

load_dotenv()

# Logger configuration
filepath = pathlib.Path(__file__).parent.absolute()
logging.basicConfig(
    filename=f"{filepath}/finelady.log",
    level=logging.INFO,
)
_logger = logging.getLogger("finelady_logger")
_logger.info(f"FineLadyBot inititated at {datetime.now()}")

db = Database("finelady", _logger)


def run() -> None:
    praw_config = PrawConfig()
    reddit = praw.Reddit(
        client_id=praw_config.client_id,
        client_secret=praw_config.client_secret,
        user_agent=praw_config.user_agent,
        username=praw_config.username,
        password=praw_config.password,
    )

    opt_out_list = db.query_users()
    sub_opt_out_list = db.query_subs()

    submission_stream: SubredditStream = reddit.subreddit("all").stream.submissions(pause_after=-1)
    message_stream: Iterator[Union["praw.models.Comment", "praw.models.Message"]] = reddit.inbox.stream(
        pause_after=-1, skip_existing=1
    )

    submission: Submission
    message: Message
    while True:
        title_cache = []
        max_cache_size = 20
        for submission in submission_stream:
            if submission is None:
                break
            if "banbury" in submission.title.lower() and submission.subreddit != "banbury":
                if (
                    submission.author.name not in opt_out_list
                    and submission.subreddit.display_name not in sub_opt_out_list
                    and submission.title not in title_cache
                ):
                    crosspost_submission(submission)
                    title_cache.append(submission.title)
                    if len(title_cache) > max_cache_size:
                        title_cache.pop(0)

        for message in message_stream:
            if message is None:
                break
            if "user_opt_out" in message.subject:
                message_date = datetime.fromtimestamp(message.created_utc)
                db.add_opt_out_user(message.author.name, message_date)
            if "sub_opt_out" in message.subject:
                parse_sub_opt_out(message, reddit)


def get_opt_out_url() -> str:
    user = "FineLadyBot"
    subject = quote_plus("user_opt_out")
    message = quote_plus("Please do not cross-post my reddit submissions to /r/banbury in the future.")
    direct_message_url = f"https://www.reddit.com/message/compose?to={user}&subject={subject}&message={message}"
    return direct_message_url


def get_sub_opt_out_url(subreddit: Subreddit) -> str:
    user = "FineLadyBot"
    subject = quote_plus("sub_opt_out")
    message = quote_plus(f"Please do not post anything further to /r/{subreddit}")
    direct_message_url = f"https://www.reddit.com/message/compose?to={user}&subject={subject}&message={message}"
    return direct_message_url


def parse_submission(submission: Submission) -> ParsedSubmission:
    subreddit: Subreddit = submission.subreddit
    parsed_submission = ParsedSubmission(
        subreddit=subreddit,
        opt_out_url=get_opt_out_url(),
        sub_opt_out_url=get_sub_opt_out_url(subreddit),
        title=submission.title,
        url=submission.url,
        cross_post_title=f"{submission.title} [cross-posted from /r/{subreddit}]",
    )
    return parsed_submission


def crosspost_submission(submission: Submission) -> None:
    """Cross-post a submission to /r/banbury, and reply to the original submission"""
    parsed_submission = parse_submission(submission)
    crosspost: Submission = submission.crosspost(
        subreddit="banbury",
        title=parsed_submission.cross_post_title,
        send_replies=False,
    )

    msg = f"""This post has been [cross-posted to /r/banbury]({crosspost.permalink}).
        \n\n_This action was completed by a bot. You can opt-out from your posts 
        being cross-posted by clicking [here]({parsed_submission.opt_out_url})_
        \n\n_If you're a moderator and don't want this bot appearing on this sub, please click
        [here]({parsed_submission.sub_opt_out_url})_"""

    submission.reply(msg)
    _logger.info(
        f"[{datetime.now()}]Cross-posted '{parsed_submission.title}' from {parsed_submission.subreddit} to /r/banbury URL: {parsed_submission.url}"
    )


def parse_sub_opt_out(message: Message, reddit: praw.Reddit) -> None:
    """Parse a request to opt out from being cross-posted by a sub moderator.
    Add the request to the database."""
    message_date = datetime.fromtimestamp(message.created_utc)
    subreddit = reddit.subreddit(regex.search(r"(?<=/r/)\w*", message.body).group(0))
    if subreddit:
        subreddit_moderators = [mod for mod in subreddit.moderator()]
        from_mod = message.author.name in subreddit_moderators
        if from_mod:
            db.add_opt_out_sub(subreddit.display_name, message.author.name, message_date)
