from urllib import response
from tests.conftest import data_test, test_client


class TestDeleteŴordsEndpoint:
    def test_delete_first_word(
        self,
        populate_mongo: None,
    ) -> None:
        response = test_client.delete(f"/api/v1/words/{data_test[0]}")
        assert response.status_code == 204

        get_response = test_client.get("/api/v1/words")
        expected_response = data_test[1:]
        assert get_response.status_code == 200
        assert get_response.json()["data"] == expected_response

    def test_delete_word_in_the_middle(
        self,
        populate_mongo: None,
    ) -> None:
        response = test_client.delete(f"/api/v1/words/{data_test[3]}")
        assert response.status_code == 204

        get_response = test_client.get("/api/v1/words")
        expected_response = data_test[0:3] + data_test[4:]
        assert get_response.status_code == 200
        assert get_response.json()["data"] == expected_response

    def test_delete_last_word(
        self,
        populate_mongo: None,
    ) -> None:
        response = test_client.delete(f"/api/v1/words/{data_test[-1]}")
        assert response.status_code == 204

        get_response = test_client.get("/api/v1/words")
        expected_response = data_test[:-1]
        assert get_response.status_code == 200
        assert get_response.json()["data"] == expected_response

    def test_delete_non_existing_word(
        self,
        populate_mongo: None,
    ) -> None:
        response = test_client.delete("/api/v1/words/invented")
        assert response.status_code == 404
