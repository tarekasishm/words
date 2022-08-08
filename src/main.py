from typing import Any, Dict, Final, List
from fastapi import FastAPI, APIRouter

from src.health_check.infrastructure.api_controllers import health_checks

API_V: Final[str] = "/api/v1"
tags_metadata: List[Dict[str, Any]] = [
    {"name": "Template API", "description": "API Template"}
]


app = FastAPI(
    title="API Template",
    openapi_url=f"{API_V}/openapi.json",
    openapi_tags=tags_metadata,
)

api_router = APIRouter()

api_router.include_router(
    health_checks.router, prefix="/health-check", tags=["HealthCheck"]
)

app.include_router(api_router, prefix=API_V)
