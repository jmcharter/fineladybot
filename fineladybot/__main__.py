import click
from fineladybot import finelady


@click.group(invoke_without_command=True, help="CLI tool to run fineladybot and access related data.")
@click.pass_context
def cli(ctx: click.Context):
    if ctx.invoked_subcommand is None:
        run()


@cli.command()
def run():
    finelady.run()


@cli.command()
@click.argument("get_type")
def get(get_type: str):
    """Get GET_TYPE data.

    GET_TYPE is either 'users' or 'subs'."""
    if get_type == "users":
        users = finelady.db.query_users()
        if not users:
            click.echo("No users have been added to the ban list.")
            return
        for user in users:
            click.echo(user)
    if get_type == "subs":
        subs = finelady.db.query_subs()
        if not subs:
            click.echo("No subs have been added to the ban list.")
            return
        for sub in subs:
            click.echo(sub)
    else:
        click.echo("GET_TYPE must be 'users' or 'subs'. If you're unsure use --help")


if __name__ == "__main__":
    cli()
