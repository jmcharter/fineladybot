#!/usr/bin/python3
import praw, logging, pathlib, os
from dotenv import load_dotenv
from datetime import datetime
from urllib.parse import quote_plus
from database import database

load_dotenv()

# Logger configuration
filepath = pathlib.Path(__file__).parent.absolute()
logging.basicConfig(
    filename=f"{filepath}/finelady.log",
    level=logging.INFO,
)
_logger = logging.getLogger("finelady_logger")
_logger.info(f"FineLadyBot inititated at {datetime.now()}")

db = database("finelady", _logger)


def main():
    reddit = praw.Reddit(
        client_id=os.environ.get("CLIENT_ID"),
        client_secret=os.environ.get("CLIENT_SECRET"),
        user_agent=os.environ.get("REDDIT_USER_AGENT"),
        username=os.environ.get("REDDIT_USERNAME"),
        password=os.environ.get("REDDIT_PASSWORD"),
    )

    opt_out_list = db.query_users()

    submission_stream = reddit.subreddit("all").stream.submissions(pause_after=-1)
    message_stream = reddit.inbox.stream(pause_after=-1)

    while True:
        for submission in submission_stream:
            if submission is None:
                break
            if (
                "banbury" in submission.title.lower()
                and submission.subreddit != "banbury"
            ):
                if submission.author.name not in opt_out_list:
                    parse_submission(submission)

        for message in message_stream:
            if message is None:
                break
            if "opt_out" in message.subject:
                message_date = datetime.fromtimestamp(message.created_utc)
                db.add_opt_out_user(message.author.name, message_date)


def get_opt_out_url():
    user = "FineLadyBot"
    subject = quote_plus("opt_out")
    message = quote_plus(
        "Please do not cross-post my reddit submissions to /r/banbury in the future."
    )
    direct_message_url = f"https://www.reddit.com/message/compose?to={user}&subject={subject}&message={message}"
    return direct_message_url


def parse_submission(submission):
    opt_out_url = get_opt_out_url()
    subreddit = submission.subreddit
    title = submission.title
    url = submission.url
    cross_post_title = f"{title} [crossposted from /r/{subreddit}]"
    crosspost = submission.crosspost(
        subreddit="banbury", title=cross_post_title, send_replies=False
    )
    submission.reply(
        f"This post has been [cross-posted to /r/banbury]({crosspost.permalink}).\n\n_This action was completed by a bot. You can opt-out from your posts being crossposted by clicking [here]({opt_out_url})_"
    )
    _logger.info(
        f"[{datetime.now()}]Cross-posted '{title}' from {subreddit} to /r/banbury URL: {url}"
    )


if __name__ == "__main__":
    main()
