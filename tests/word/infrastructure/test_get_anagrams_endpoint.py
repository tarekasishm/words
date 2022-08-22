from typing import Dict, List
import os

import pytest

from tests.conftest import data_test, test_client


class TestGetAnagramsEndpoint:
    @pytest.mark.skipif( not os.getenv("RUN_VALIDATION_TEST", False), reason="Environment not ready" )
    def test_get_anagrams_succesfully(
        self,
        populate_mongo: None,
    ) -> None:
        response = test_client.get(f"/api/v1/words/asco/anagrams")
        assert response.status_code == 200

        expected_response: Dict[str, List[str]] = {"data": ["cosa", "caso"]}
        assert sorted(response.json()["data"]) == sorted(expected_response["data"])

    @pytest.mark.skipif( not os.getenv("RUN_VALIDATION_TEST", False), reason="Environment not ready" )
    def test_not_found_anagrams(
        self,
        populate_mongo: None,
    ) -> None:
        response = test_client.get(f"/api/v1/words/carro/anagrams")
        assert response.status_code == 200

        expected_response: Dict[str, List[str]] = {"data": []}
        assert response.json() == expected_response

    @pytest.mark.skipif( not os.getenv("RUN_VALIDATION_TEST", False), reason="Environment not ready" )
    def test_get_anagrams_without_including_same_word(
        self,
        populate_mongo: None,
    ) -> None:
        response = test_client.get(f"/api/v1/words/cosa/anagrams")
        assert response.status_code == 200

        expected_response: Dict[str, List[str]] = {"data": ["caso"]}
        assert response.json() == expected_response
