# !/usr/bin/python3
import praw, logging, pathlib, os, regex
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
    sub_opt_out_list = db.query_subs()

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
                if (
                    submission.author.name not in opt_out_list
                    and submission.subreddit.display_name not in sub_opt_out_list
                ):
                    parse_submission(submission)

        for message in message_stream:
            if message is None:
                break
            if "user_opt_out" in message.subject:
                message_date = datetime.fromtimestamp(message.created_utc)
                db.add_opt_out_user(message.author.name, message_date)
            if "sub_opt_out" in message.subject:
                parse_sub_opt_out(message, reddit)
                print("Opting out sub")


def get_opt_out_url():
    user = "FineLadyBot"
    subject = quote_plus("user_opt_out")
    message = quote_plus(
        "Please do not cross-post my reddit submissions to /r/banbury in the future."
    )
    direct_message_url = f"https://www.reddit.com/message/compose?to={user}&subject={subject}&message={message}"
    return direct_message_url


def get_sub_opt_out_url(subreddit):
    user = "FineLadyBot"
    subject = quote_plus("sub_opt_out")
    message = quote_plus(f"Please do not post anything further to /r/{subreddit}")
    direct_message_url = f"https://www.reddit.com/message/compose?to={user}&subject={subject}&message={message}"
    return direct_message_url


def parse_submission(submission):
    subreddit = submission.subreddit
    opt_out_url = get_opt_out_url()
    sub_opt_out_url = get_sub_opt_out_url(subreddit)
    title = submission.title
    url = submission.url
    cross_post_title = f"{title} [cross-posted from /r/{subreddit}]"
    crosspost = submission.crosspost(
        subreddit="banbury", title=cross_post_title, send_replies=False
    )
    submission.reply(
        f"""This post has been [cross-posted to /r/banbury]({crosspost.permalink}).
        \n\n_This action was completed by a bot. You can opt-out from your posts 
        being cross-posted by clicking [here]({opt_out_url})_
        \n\n_If you're a moderator and don't want this bot appearing on this sub, please click
        [here]({sub_opt_out_url})_"""
    )
    _logger.info(
        f"[{datetime.now()}]Cross-posted '{title}' from {subreddit} to /r/banbury URL: {url}"
    )


def parse_sub_opt_out(message, reddit):
    message_date = datetime.fromtimestamp(message.created_utc)
    subreddit = reddit.subreddit(regex.search(r"(?<=/r/)\w*", message.body).group(0))
    print(subreddit)
    if subreddit:
        subreddit_moderators = [mod for mod in subreddit.moderator()]
        print(subreddit_moderators)
        from_mod = message.author.name in subreddit_moderators
        print(from_mod)
        if from_mod:
            db.add_opt_out_sub(
                subreddit.display_name, message.author.name, message_date
            )


if __name__ == "__main__":
    main()
