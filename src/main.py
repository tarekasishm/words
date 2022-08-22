from typing import Any, Dict, Final, List
from fastapi import FastAPI, APIRouter

from src.shared.infrastructure.persistance.mongo_client import MongoClient
from src.health_check.infrastructure.api_controllers import health_checks
from src.word.infrastructure.api_controllers import words
from src.word.infrastructure.persistance.word_index import create_word_index

API_V: Final[str] = "/api/v1"
tags_metadata: List[Dict[str, Any]] = [
    {"name": "WORDS API", "description": "Awesome WORDS API"}
]


async def on_start_up() -> None:
    mongo_client = await MongoClient.get_client()
    await create_word_index(mongo_client)

app = FastAPI(
    title="WORDS API",
    openapi_url=f"{API_V}/openapi.json",
    openapi_tags=tags_metadata,
    on_startup=[on_start_up],
)

api_router = APIRouter()

api_router.include_router(
    health_checks.router, prefix="/health-check", tags=["HealthCheck"]
)
api_router.include_router(words.router, prefix="/words", tags=["Words"])

app.include_router(api_router, prefix=API_V)
