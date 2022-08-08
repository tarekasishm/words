from typing import Dict

from fastapi.responses import JSONResponse

from src.shared.domain.exceptions import (
    INVALID_FIELD,
    NOT_FOUND,
    DEPENDENCY_PROBLEM,
    CONFLICT,
    NOT_ACCEPTABLE,
)

class JsonResponseBuilder:
    ERROR_CODES: Dict[str, int] = {
        INVALID_FIELD: 403,
        NOT_FOUND: 404,
        DEPENDENCY_PROBLEM: 422,
        CONFLICT: 409,
        NOT_ACCEPTABLE: 406,
    }
    @classmethod
    async def build_json_response(
        cls,
        standard_exception: str,
        exception_message: str,
    ) -> JSONResponse:
        status_code: int = cls.ERROR_CODES.get(standard_exception, 400)
        return JSONResponse(
            status_code=status_code,
            content={"message": exception_message},
        )
