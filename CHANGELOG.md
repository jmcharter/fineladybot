# Changelog

## 1.0.0
- Rework stream parsing to handle submissions and inbox messages
- Create a database to store opt-outs if one doesn't exist
- Allow users to add themselves to the opt-out list by messaging the bot with subject "opt-out"

## 0.4.1
- Add requirements.txt

## 0.4.0
- Add link to submission comment allowing users to opt-out

## 0.3.1
- Move credentials to be read from .env file

## 0.3.0
- Add logger to aid debugging

## 0.2.1
- Add MIT License

## 0.2.0
- Bot identifies it's posts with the tag "[Cross-post from \<subreddit\>]"
- Comment on original submission to share the cross-posted link

## 0.1.2
- Make searches case-agnostic (i.e searches for 'Banbury', 'banbury', 'bANBURY', etc)

## 0.1.1
- Scan all new Reddit submissions for term "Banbury"
- Cross-post found submissions to /r/banbury

## 0.1.0
- Initial creation