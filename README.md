# FineLadyBot
![version](https://img.shields.io/badge/Version-1.0.1-informational)
![license-MIT](https://img.shields.io/github/license/jmcharter/fineladybot)

FineLadyBot is a bot that runs on behalf of [/r/banbury](https://reddit.com/r/banbury), which is a subreddit for discussion of town in Oxfordshire, UK.

In it's current state, the bot will scrape all new Reddit submissions and look for mentions of 'banbury'. If it finds one, it will cross-post the submission to /r/banbury and comment on the original submission with a link.

This occasionally results in false positives, where somebody with the surname 'Banbury' is the subject of the submission, or other non-UK locations are the subject.

There is also potential for abuse with this. Given the size of the sub and the relative obscurity of the town though, I don't consider this a massive concern at present, but I do intend to address this at some point in the future.

## Usage
Simply install the bot and run the script. 

Due to the nature of PRAW, the script is likely to crash semi-frequently either due to Reddit going down or other API related errors. Given this, I'd suggest setting this up on some type of cron job or as a daemon that restarts on crash.

## Installation

Currently, your best bet it to simply clone the repo and host the bot either locally or on some kind of server or cloud platform.

## Dependencies

The bot is written in Python and uses the [PRAW Library](https://praw.readthedocs.io/en/stable/).

## TO-DO
- [X] Store opt-out requests
- [X] Automatically add opt-out requests from messages sent to inbox
- [ ] Store a list of subreddits to avoid
- [ ] Allow subreddit mods to add their sub to the "banlist"

