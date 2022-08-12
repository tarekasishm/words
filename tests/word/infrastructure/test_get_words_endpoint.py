from tests.conftest import data_test, test_client


class TestGetWordsEndpoint:
    def test_get_all_words(self, populate_mongo: None) -> None:
        response = test_client.get("/api/v1/words", params={"limit": 10, "offset": 0})
        assert response.status_code == 200
        assert response.json()["data"] == data_test

    def test_get_paginated_words(self, populate_mongo: None) -> None:
        response = test_client.get("/api/v1/words", params={"limit": 3, "offset": 2})
        assert response.status_code == 200
        assert response.json()["data"] == data_test[2:5]

    def test_invalid_offset_value(
        self,
        populate_mongo: None,
    ) -> None:
        response = test_client.get("/api/v1/words", params={"offset": -1})

        assert response.status_code == 403
        assert (
            response.json()["message"] == "Offset must be greater than or equal to zero"
        )

    def test_invalid_limit_value(
        self,
        populate_mongo: None,
    ) -> None:
        response = test_client.get("/api/v1/words", params={"limit": 0})

        assert response.status_code == 403
        assert response.json()["message"] == "Limit must be a positive integer"
