from pydantic import BaseModel, BaseSettings, Field
import praw.models


class PrawConfig(BaseSettings):
    client_id: str = Field(..., env="CLIENT_ID", description="Reddit Client ID")
    client_secret: str = Field(..., env="CLIENT_SECRET", description="Reddit Client Secret")
    user_agent: str = Field(..., env="REDDIT_USER_AGENT", description="Reddit User Agent")
    username: str = Field(..., env="REDDIT_USERNAME", description="Reddit Bot Account's Username")
    password: str = Field(..., env="REDDIT_PASSWORD", description="Reddit Bot Account's Password")


class ParsedSubmission(BaseModel):
    subreddit: praw.models.Subreddit
    opt_out_url: str
    sub_opt_out_url: str
    title: str
    url: str
    cross_post_title: str
