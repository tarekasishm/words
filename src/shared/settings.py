from pydantic import BaseSettings


class Settings(BaseSettings):
    mongo_uri: str
    mongo_user: str
    mongo_pass: str
