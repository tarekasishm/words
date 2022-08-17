import asyncio
from typing import Any, AsyncGenerator, Dict, Optional

from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorClientSession

from src.shared.settings import Settings


class MongoClient:
    _mongo_client: Optional[AsyncIOMotorClient] = None
    _settings: Dict[str, Any] = Settings().dict()

    @classmethod
    async def get_client(cls) -> AsyncIOMotorClient:
        if cls._mongo_client is None:
            cls._mongo_client = AsyncIOMotorClient(
                host=cls._settings["mongo_uri"],
                username=cls._settings["mongo_user"],
                password=cls._settings["mongo_pass"],
            )
            # workaround: https://github.com/encode/starlette/issues/1315
            cls._mongo_client.get_io_loop = asyncio.get_event_loop
        return cls._mongo_client

    @classmethod
    async def get_session(cls) -> AsyncGenerator[AsyncIOMotorClientSession, None]:
        try:
            if cls._mongo_client is None:
                cls._mongo_client = AsyncIOMotorClient(
                    host=cls._settings["mongo_uri"],
                    username=cls._settings["mongo_user"],
                    password=cls._settings["mongo_pass"],
                )
            db_session: Optional[
                AsyncIOMotorClientSession
            ] = await cls._mongo_client.start_session()
            yield db_session
        except:
            import traceback
            traceback.print_exc()
            db_session = None
            raise HTTPException(503, detail="Service not available, please try later.")
        finally:
            if db_session:
                await db_session.end_session()
