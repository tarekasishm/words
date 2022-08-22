from motor.motor_asyncio import AsyncIOMotorClient

from src.shared.settings import Settings

async def create_word_index(mongo_client: AsyncIOMotorClient):
    settings: Settings = Settings()
    await mongo_client[settings.words_db][settings.words_collection].create_index(
        "anagram"
    )
