from typing import Optional, Union
from venv import create

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClientSession

from src.shared.application.application_exceptions import (
    ApplicationException,
)
from src.shared.infrastructure.api_controllers.json_exceptions.json_response_builder import (
    JsonResponseBuilder,
)
from src.shared.infrastructure.persistance.mongo_client import get_mongo_client
from src.word.application.create_word_use_case import CreateWordUseCase
from src.word.application.stored_word_dto import StoredWordDto
from src.word.infrastructure.persistance.stored_word_mongo_repository import (
    StoredWordMongoRepository,
)

router = APIRouter()


@router.post(
    "",
    response_model=StoredWordDto,
    status_code=200,
    description="Get words",
)
async def get_words_controller(
    create_word_dto: StoredWordDto,
    mongo_client: AsyncIOMotorClientSession = Depends(get_mongo_client),
) -> Union[StoredWordDto, JSONResponse]:
    try:
        stored_word_mongo_repository: StoredWordMongoRepository = (
            StoredWordMongoRepository(mongo_client)
        )
        create_word_use_case: CreateWordUseCase = CreateWordUseCase(
            stored_word_mongo_repository,
        )
        return await create_word_use_case.create(create_word_dto)
    except ApplicationException as application_exception:
        json_response: JSONResponse = await JsonResponseBuilder.build_json_response(
            application_exception.standard_exception,
            application_exception.exception_message,
        )
        return json_response
