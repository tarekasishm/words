from typing import Optional, Union

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.shared.application.application_exceptions import (
    ApplicationException,
)

router = APIRouter()


@router.get("/", summary="Health check", status_code=200)
async def hello_world_endpoint() -> Union[Optional[str], JSONResponse]:
    try:
        return "Ok!"
    except ApplicationException:
        return JSONResponse(status_code=404, content={"message": ""})
