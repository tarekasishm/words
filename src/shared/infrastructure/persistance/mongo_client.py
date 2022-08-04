from typing import Any, AsyncGenerator, Dict
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorClientSession

from src.shared.settings import Settings

settings: Dict[str, Any] = Settings().dict()

mongo_client: AsyncIOMotorClient = AsyncIOMotorClient(
    host=settings["mongo_host"],
    port=settings["mongo_port"],
    user=settings["mongo_user"],
    password=settings["mongo_pass"],
)


async def get_mongo_client() -> AsyncGenerator[AsyncIOMotorClientSession, None]:
    try:
        db_session: AsyncIOMotorClientSession = await mongo_client.start_session()
        yield db_session
    finally:
        db_session.end_session()
