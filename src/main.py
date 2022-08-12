from typing import Any, Dict, Final, List
from fastapi import FastAPI, APIRouter

from src.shared.infrastructure.persistance.mongo_client import MongoClient
from src.health_check.infrastructure.api_controllers import health_checks
from src.word.infrastructure.api_controllers import words

API_V: Final[str] = "/api/v1"
tags_metadata: List[Dict[str, Any]] = [
    {"name": "Template API", "description": "API Template"}
]


async def on_start_up() -> None:
    await MongoClient.get_client()


app = FastAPI(
    title="API Template",
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
