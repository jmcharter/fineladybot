from pydantic import BaseModel, BaseSettings, Field, validator
from praw.models import Subreddit


class PrawConfig(BaseSettings):
    client_id: str = Field(..., env="CLIENT_ID", description="Reddit Client ID")
    client_secret: str = Field(..., env="CLIENT_SECRET", description="Reddit Client Secret")
    user_agent: str = Field(..., env="REDDIT_USER_AGENT", description="Reddit User Agent")
    username: str = Field(..., env="REDDIT_USERNAME", description="Reddit Bot Account's Username")
    password: str = Field(..., env="REDDIT_PASSWORD", description="Reddit Bot Account's Password")


class ParsedSubmission(BaseModel):
    subreddit: Subreddit = Field(..., description="Subreddit of parsed submission", validate=lambda value: value)
    opt_out_url: str
    sub_opt_out_url: str
    title: str
    url: str
    cross_post_title: str

    @validator("subreddit")
    def subreddit_is_valid(cls, value):
        if not isinstance(value, Subreddit):
            raise ValueError("subreddit must be a valid praw.models.Subreddit instance")
        return value

    class Config:
        arbitrary_types_allowed = True
