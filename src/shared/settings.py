from pydantic import BaseSettings


class Settings(BaseSettings):
    mongo_uri: str
    mongo_user: str
    mongo_pass: str
    words_db: str
    words_collection: str
