# FineLadyBot
![version](https://img.shields.io/badge/Version-2.0.0-informational)
![license-MIT](https://img.shields.io/github/license/jmcharter/fineladybot)

FineLadyBot is a bot that runs on behalf of [/r/banbury](https://reddit.com/r/banbury), which is a subreddit for discussion of town in Oxfordshire, UK.

In it's current state, the bot will scrape all new Reddit submissions and look for mentions of 'banbury'. If it finds one, it will cross-post the submission to /r/banbury and comment on the original submission with a link.

This occasionally results in false positives, where somebody with the surname 'Banbury' is the subject of the submission, or other non-UK locations are the subject.

Two tables are maintained in an SQLite database to keep track of users and subs that wish to opt out from this bots actions.

# Installation
Clone this repo and make sure you have [Poetry](https://python-poetry.org/) installed. Install the package using Poetry.

```sh
poetry install
```

# Usage

You can either run the main script and have this bot scrape and respond indefinitely, ideally through a service manager like systemd, through docker or even through a cronjo; or just from the terminal.

There is a CLI for ease of running the bot, as well as managing opt out lists.

This is a command line interface (CLI) tool for running and accessing data related to the fineladybot program. The tool allows you to list and exclude users or subreddits from the bot's cross-posting feature.

To use this tool, you need to have click and enum libraries installed.

There are three main commands available:

- run: This command runs the bot until stopped.

```sh
poetry run python fineladybot run
```

- list: This command lists either the users or subreddits that have been excluded from cross-posting. You can use the --users or --subreddits option to specify which list you want to see.

```sh
poetry run python fineladybot list --users
```

- exclude: This command allows you to add a user or subreddit to the exclusion list, so their posts are never cross-posted. You can provide the username or subreddit name using the -u or -s options respectively. If no option is provided, the tool will prompt you to choose between excluding a user or subreddit.

```sh
poetry run python fineladybot exclude -u steve
```

# Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.