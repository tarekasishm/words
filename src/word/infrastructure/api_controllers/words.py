from typing import Union
from urllib import response

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClientSession

from src.shared.application.application_exceptions import (
    ApplicationException,
)
from src.shared.infrastructure.api_controllers.json_exceptions.json_response_builder import (
    JsonResponseBuilder,
)
from src.shared.infrastructure.persistance.mongo_client import MongoClient
from src.word.application.create_word_use_case import CreateWordUseCase
from ...application.delete_word_use_case import DeleteWordUseCase
from src.word.application.get_words_use_case import GetWordsUseCase
from src.word.application.stored_word_dto import StoredWordDto
from src.word.application.update_word_use_case import UpdateWordUseCase
from src.word.application.words_dto import WordsDto
from src.word.application.word_position_dto import WordPositionDto
from src.word.infrastructure.persistance.stored_word_mongo_repository import (
    StoredWordMongoRepository,
)

router = APIRouter()


@router.post(
    "",
    response_model=StoredWordDto,
    status_code=201,
    description="Store a new word",
)
async def set_words_controller(
    create_word_dto: StoredWordDto,
    mongo_client: AsyncIOMotorClientSession = Depends(MongoClient.get_session),
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


@router.get(
    "",
    response_model=WordsDto,
    status_code=200,
    description="Get stored words",
)
async def get_words_controller(
    limit: int = Query(10),
    offset: int = Query(0),
    mongo_client: AsyncIOMotorClientSession = Depends(MongoClient.get_session),
) -> Union[WordsDto, JSONResponse]:
    try:
        stored_word_mongo_repository: StoredWordMongoRepository = (
            StoredWordMongoRepository(mongo_client)
        )
        get_words_use_case: GetWordsUseCase = GetWordsUseCase(
            stored_word_mongo_repository,
        )
        return await get_words_use_case.get_words(limit, offset)
    except ApplicationException as application_exception:
        json_response: JSONResponse = await JsonResponseBuilder.build_json_response(
            application_exception.standard_exception,
            application_exception.exception_message,
        )
        return json_response

@router.patch(
    "/{word}",
    response_model=StoredWordDto,
    status_code=200,
    description="Update position of an already stored word",
)
async def udpate_word_controller(
    word: str,
    word_position: WordPositionDto,
    mongo_client: AsyncIOMotorClientSession = Depends(MongoClient.get_session),
) -> Union[StoredWordDto, JSONResponse]:
    try:
        stored_word_mongo_repository: StoredWordMongoRepository = (
            StoredWordMongoRepository(mongo_client)
        )
        update_word_use_case: UpdateWordUseCase = UpdateWordUseCase(
            stored_word_mongo_repository,
        )

        return await update_word_use_case.update(word, word_position.position)
    except ApplicationException as application_exception:
        json_response: JSONResponse = await JsonResponseBuilder.build_json_response(
            application_exception.standard_exception,
            application_exception.exception_message,
        )
        return json_response

@router.delete(
    "/{word}",
    status_code=204,
    description="Delete word",
)
async def delete_word_controller(
    word: str,
    mongo_client: AsyncIOMotorClientSession = Depends(MongoClient.get_session),
) -> Union[None, JSONResponse]:
    try:
        stored_word_mongo_repository: StoredWordMongoRepository = (
            StoredWordMongoRepository(mongo_client)
        )
        delete_word_use_case: DeleteWordUseCase = DeleteWordUseCase(
            stored_word_mongo_repository,
        )
        return await delete_word_use_case.delete(word)
    except ApplicationException as application_exception:
        json_response: JSONResponse = await JsonResponseBuilder.build_json_response(
            application_exception.standard_exception,
            application_exception.exception_message,
        )
        return json_response