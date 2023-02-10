from pydantic import BaseSettings, Field


class Config(BaseSettings):
    hoge: str = Field(env="hoge", default="default value")
