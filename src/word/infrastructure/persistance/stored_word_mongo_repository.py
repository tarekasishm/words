from typing import Any, Callable, Coroutine, Dict, Optional

from motor.motor_asyncio import AsyncIOMotorClientSession
from pymongo.results import InsertOneResult
from pymongo.errors import ConnectionFailure, OperationFailure
from bson.objectid import ObjectId
from pymongo.read_concern import ReadConcern
from pymongo.write_concern import WriteConcern

from src.word.domain.position import Position
from src.word.domain.stored_word import StoredWord
from src.word.domain.stored_word_factory import StoredWordFactory
from src.word.domain.stored_word_repository import StoredWordRepository
from src.word.domain.word import Word
from src.shared.domain.domain_exceptions import DomainException
from src.shared.domain.exceptions import DEPENDENCY_PROBLEM
from src.shared.settings import Settings


import asyncio


class StoredWordMongoRepository(StoredWordRepository):
    def __init__(
        self,
        db_session: AsyncIOMotorClientSession,
    ) -> None:
        self.__session = db_session
        config: Dict[str, Any] = Settings().dict()
        self.__words_database: str = config["words_db"]
        self.__words_collection: str = config["words_collection"]

    async def find(
        self,
        word: Word,
    ) -> Optional[StoredWord]:
        try:
            stored_word: Optional[StoredWord] = None
            stored_word_dict: Dict[str, Any] = await self.__session.client[
                self.__words_database
            ][self.__words_collection].find_one(
                {"_id": word.word}, session=self.__session
            )
            if stored_word_dict:
                stored_word = StoredWordFactory.build(
                    stored_word_dict["_id"],
                    stored_word_dict["position"],
                )
            return stored_word
        except Exception:
            raise DomainException(
                "StoredWordRepository",
                DEPENDENCY_PROBLEM,
                "Error finding words",
            )

    async def save(
        self,
        stored_word: StoredWord,
    ) -> StoredWord:
        async with self.__session.start_transaction():
            return await self._run_transaction_with_retry(self._save, stored_word)

    async def _save(
        self,
        stored_word: StoredWord,
    ) -> StoredWord:
        last_position: Optional[Position] = None
        last_word: Optional[Word] = None
        async for last_stored_word in self.__session.client[self.__words_database][
            self.__words_collection
        ].find({}, session=self.__session).sort("position", -1).limit(1):
            last_position = Position(last_stored_word["position"])
            last_word = Word(last_stored_word["_id"])

        # select for update
        if last_word:
            await self.__session.client[self.__words_database][
                self.__words_collection
            ].find_one_and_update(
                {
                    "_id": last_word.word,
                },
                {"$set": {"Lock": ObjectId()}},
                session=self.__session,
            )
        inserted_position: Position = Position(stored_word.position)
        if last_position is None:
            inserted_position = Position(1)
        if last_position and inserted_position > last_position:
            inserted_position = Position(last_position.position + 1)

        await self.__session.client[self.__words_database][
            self.__words_collection
        ].insert_one(
            {"_id": stored_word.word, "position": inserted_position.position},
            session=self.__session,
        )
        if last_position and last_position > inserted_position:
            await self.__session.client[self.__words_database][
                self.__words_collection
            ].update_many(
                {
                    "position": {"$gte": inserted_position.position},
                    "_id": {"$ne": stored_word.word},
                },
                {"$inc": {"position": 1}},
                session=self.__session,
            )
        return StoredWordFactory.build(stored_word.word, inserted_position.position)

    async def _run_transaction_with_retry(
        self,
        txn_coro: Callable[[StoredWord], Coroutine[Any, Any, StoredWord]],
        stored_word: StoredWord,
    ) -> StoredWord:
        while True:
            try:
                real_stored_word: StoredWord = await txn_coro(
                    stored_word
                )  # performs transaction
                return real_stored_word
            except (ConnectionFailure, OperationFailure) as exc:

                # If transient error, retry the whole transaction
                if exc.has_error_label("TransientTransactionError"):
                    continue
                raise DomainException(
                    "StoredWordRepository",
                    DEPENDENCY_PROBLEM,
                    "Service not available. Please try later.",
                )
            except Exception:
                raise DomainException(
                    "StoredWordRepository",
                    DEPENDENCY_PROBLEM,
                    "Service not available. Please try later.",
                )
