from collections import Counter
from typing import Any, AsyncGenerator, Dict, List

import pytest
from asgi_lifespan import LifespanManager
from fastapi.testclient import TestClient
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

from src.main import app
from src.shared.settings import Settings

test_client = TestClient(app)

data_test: List[str] = [
    "cosa",
    "caso",
    "paco",
    "pepe",
    "calle",
    "málaga",
]
data_dict: List[Dict[str, Any]] = [
    {"_id": data, "position": idx + 1, "anagram": dict(Counter(sorted(data)))} for idx, data in enumerate(data_test)
]


@pytest.fixture()
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            yield ac


@pytest.fixture()
async def populate_mongo() -> AsyncGenerator[None, None]:
    settings: Dict[str, Any] = Settings().dict()

    mongo_client: AsyncIOMotorClient = AsyncIOMotorClient(
        host=settings["mongo_uri"],
        username=settings["mongo_user"],
        password=settings["mongo_pass"],
    )
    await mongo_client[settings["words_db"]][settings["words_collection"]].drop()
    await mongo_client[settings["words_db"]][settings["words_collection"]].insert_many(
        data_dict,
    )
    yield
