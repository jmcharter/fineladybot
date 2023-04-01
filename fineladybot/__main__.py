from datetime import datetime
from enum import Enum
import click
from fineladybot import finelady


class Choice(str, Enum):
    USER = "user"
    SUBREDDIT = "subreddit"


@click.group(invoke_without_command=True, help="CLI tool to run fineladybot and access related data.")
@click.pass_context
def cli(ctx: click.Context):
    if ctx.invoked_subcommand is None:
        run()


@cli.command()
def run():
    """Run the bot until stopped."""
    finelady.run()


@cli.command()
@click.option("-u", "--users", "user_flag", is_flag=True)
@click.option("-s", "--subreddits", "subreddit_flag", is_flag=True)
def list(user_flag: bool, subreddit_flag: bool):
    """Lists either user or subreddits from exclusion list"""
    if user_flag and subreddit_flag:
        click.echo("Please only use option --users or --subreddits")
    if user_flag:
        users = finelady.db.query_users()
        if not users:
            click.echo("No users have been added to the ban list.")
            return
        for user in users:
            click.echo(user)
    if subreddit_flag:
        subs = finelady.db.query_subs()
        if not subs:
            click.echo("No subs have been added to the ban list.")
            return
        for sub in subs:
            click.echo(sub)
    else:
        click.echo("Use list --help for options to list")


@cli.command()
@click.option(
    "-u",
    "--user",
    prompt="Enter the username of the user to exclude",
    prompt_required=False,
    help="Add a user to the exclusion list, so their posts are never cross-posted",
)
@click.option(
    "-s",
    "--subreddit",
    prompt_required=False,
    prompt="Enter the name of the subreddit to exclude",
    help="Add a subreddit to the exclusion list, so posts from there are never cross-posted",
)
def exclude(user, subreddit):
    def exclude_user(user):
        finelady.db.add_opt_out_user(user, datetime.now())

    def exclude_subreddit(subreddit):
        finelady.db.add_opt_out_sub(subreddit, "FINELADY", datetime.now())

    if user and subreddit:
        click.echo("Please only provide user or subreddit, not both.")
    if user:
        exclude_user(user)
    elif subreddit:
        exclude_subreddit(subreddit)
    else:
        choice = click.prompt(
            "Exclude user or subreddit?",
            type=click.Choice([Choice.USER.value, Choice.SUBREDDIT.value], case_sensitive=False),
        )
        if choice == Choice.USER.value:
            exclude_user(user)
        if choice == Choice.SUBREDDIT.value:
            exclude_subreddit(subreddit)


if __name__ == "__main__":
    cli()
