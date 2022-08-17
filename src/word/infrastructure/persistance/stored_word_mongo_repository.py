from typing import Any, Callable, Coroutine, Dict, List, Optional

from motor.motor_asyncio import AsyncIOMotorClientSession
from pymongo.errors import ConnectionFailure, OperationFailure
from pymongo.results import DeleteResult
from bson.objectid import ObjectId

from src.shared.domain.limit import Limit
from src.shared.domain.offset import Offset
from src.word.domain.anagram_validator import AnagramValidator
from src.word.domain.position import Position
from src.word.domain.stored_word import StoredWord
from src.word.domain.stored_word_factory import StoredWordFactory
from src.word.domain.stored_word_repository import StoredWordRepository
from src.word.domain.word import Word
from src.shared.domain.domain_exceptions import DomainException
from src.shared.domain.exceptions import DEPENDENCY_PROBLEM, NOT_FOUND
from src.shared.settings import Settings


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

    async def find_words(
        self,
        limit: Limit,
        offset: Offset,
    ) -> List[StoredWord]:
        try:
            stored_words: List[StoredWord] = []
            async for word in self.__session.client[self.__words_database][
                self.__words_collection
            ].find(
                {
                    "position": {
                        "$gt": offset.offset,
                        "$lte": offset.offset + limit.limit,
                    }
                },
                session=self.__session,
            ).sort(
                "position", 1
            ):
                stored_words.append(
                    StoredWordFactory.build(
                        word["_id"],
                        word["position"],
                    )
                )
            return stored_words
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

    async def update(
        self,
        stored_word: StoredWord,
    ) -> StoredWord:
        async with self.__session.start_transaction():
            return await self._run_transaction_with_retry(self._update, stored_word)

    async def delete(
        self,
        word: Word,
    ) -> None:
        try:
            current_word: Optional[StoredWord] = await self.find(word)
            if current_word is None:
                raise DomainException(
                    "StoredWordMongoRepository",
                    NOT_FOUND,
                    f"{word.word} not found",
                )
            async with self.__session.start_transaction():
                await self._run_transaction_with_retry(self._delete, current_word)
        except DomainException as domain_exception:
            raise domain_exception
        except Exception:
            raise DomainException(
                "StoredWordRepository",
                DEPENDENCY_PROBLEM,
                "Error deleting words",
            )

    async def find_anagrams(
        self,
        word: Word,
    ) -> List[StoredWord]:
        try:
            anagrams: List[StoredWord] = []
            async for stored_word_dict in self.__session.client[ 
                self.__words_database
            ][self.__words_collection].find({}, session=self.__session):
                if AnagramValidator.is_anagram(word, Word(stored_word_dict["_id"])):
                    anagrams.append(
                        StoredWordFactory.build(
                            stored_word_dict["_id"],
                            stored_word_dict["position"],
                        )
                    )
            return anagrams
        except DomainException as domain_exception:
            raise DomainException(
                domain_exception.domain_artifact,
                domain_exception.standard_exception,
                domain_exception.exception_message,
            )

    async def _delete(
        self,
        current_word: StoredWord,
    ) -> StoredWord:
        try:

            delete_result: DeleteResult = await self.__session.client[
                self.__words_database
            ][self.__words_collection].delete_one(
                {"_id": current_word.word}, session=self.__session
            )
            if delete_result.deleted_count != 1:
                raise DomainException(
                    "StoredWordMongoRepository",
                    NOT_FOUND,
                    f"{current_word.word} could not be deleted",
                )
            await self.__session.client[self.__words_database][
                self.__words_collection
            ].update_many(
                {"position": {"$gt": current_word.position}},
                {"$inc": {"position": -1}},
                session=self.__session,
            )
            return current_word
        except DomainException as domain_exception:
            raise domain_exception
        except Exception:
            raise DomainException(
                "StoredWordRepository",
                DEPENDENCY_PROBLEM,
                "Error deleting words",
            )

    async def _update(
        self,
        new_stored_word: StoredWord,
    ) -> StoredWord:
        # ToDo: check returned values
        current_word: Optional[StoredWord] = await self.find(Word(new_stored_word.word))
        if current_word is None:
            raise DomainException(
                "StoredWordMongoRepostiory",
                NOT_FOUND,
                f"{new_stored_word.word} not found",
            )
        if current_word == new_stored_word:
            return current_word
        inserted_position: Position = await self._select_for_update_last_word(
            new_stored_word
        )
        inserted_position = (
            inserted_position
            if inserted_position.position == new_stored_word.position
            else Position(inserted_position.position - 1)
        )
        query: Dict[str, Any] = {
            "position": {
                "$gt": current_word.position,
                "$lte": inserted_position.position,
            }
        }
        update: Dict[str, Any] = {"$inc": {"position": -1}}
        if inserted_position.position < current_word.position:
            query = {
                "position": {
                    "$gte": inserted_position.position,
                    "$lte": current_word.position,
                }
            }
            update = {"$inc": {"position": 1}}
        await self.__session.client[self.__words_database][
            self.__words_collection
        ].update_many(query, update, session=self.__session)
        await self.__session.client[self.__words_database][
            self.__words_collection
        ].update_one(
            {"_id": new_stored_word.word},
            {"$set": {"position": inserted_position.position}},
            session=self.__session,
        )
        return StoredWordFactory.build(new_stored_word.word, inserted_position.position)

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
        if last_position and inserted_position <= last_position:
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
                    stored_word,
                )  # performs transaction
                return real_stored_word
            except (ConnectionFailure, OperationFailure) as exc:
                import traceback

                traceback.print_exc()
                # If transient error, retry the whole transaction
                if exc.has_error_label("TransientTransactionError"):
                    continue
                raise DomainException(
                    "StoredWordRepository",
                    DEPENDENCY_PROBLEM,
                    "Service not available. Please try later.",
                )
            except Exception:
                import traceback

                traceback.print_exc()
                raise DomainException(
                    "StoredWordRepository",
                    DEPENDENCY_PROBLEM,
                    "Service not available. Please try later.",
                )

    async def _select_for_update_last_word(
        self,
        stored_word: StoredWord,
    ) -> Position:
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
        return inserted_position
