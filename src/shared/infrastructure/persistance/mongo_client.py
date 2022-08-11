from typing import Any, AsyncGenerator, Dict, Optional

from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorClientSession

from src.shared.settings import Settings

settings: Dict[str, Any] = Settings().dict()

mongo_client: AsyncIOMotorClient = AsyncIOMotorClient(
    host=settings["mongo_uri"],
    username=settings["mongo_user"],
    password=settings["mongo_pass"],
)


async def get_mongo_client() -> AsyncGenerator[AsyncIOMotorClientSession, None]:
    try:
        db_session: Optional[AsyncIOMotorClientSession] = await mongo_client.start_session()
        yield db_session
    except:
        db_session = None
        raise HTTPException(503, detail="Service not available, please try later.")
    finally:
        if db_session:
            await db_session.end_session()