from typing import Optional, Union

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.shared.infrastructure.api_controllers.json_exceptions.responses import (
    NOT_FOUND_STATUS_CODE,
)
from src.shared.application.application_exceptions import (
    ApplicationException,
)

router = APIRouter()


@router.get("/", summary="Health check", status_code=200)
async def hello_world_endpoint() -> Union[Optional[str], JSONResponse]:
    try:
        return "Ok!"
    except ApplicationException:
        return JSONResponse(status_code=NOT_FOUND_STATUS_CODE, content={"message": ""})
