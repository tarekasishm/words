from tests.conftest import data_test, test_client


class TestPatchWordsEndpoint:
    def test_patch_word_to_higher_position(
        self,
        populate_mongo: None,
    ) -> None:
        response = test_client.patch(
            f"/api/v1/words/{data_test[2]}", json={"position": 5}
        )
        assert response.status_code == 200
        assert response.json() == {"word": data_test[2], "position": 5}

        get_response = test_client.get("/api/v1/words")
        expected_response = (
            data_test[0:2] + data_test[3:5] + [data_test[2]] + data_test[5:]
        )
        assert get_response.status_code == 200
        assert get_response.json()["data"] == expected_response

    def test_patch_word_to_lower_position(
        self,
        populate_mongo: None,
    ) -> None:
        response = test_client.patch(
            f"/api/v1/words/{data_test[4]}", json={"position": 2}
        )
        assert response.status_code == 200
        assert response.json() == {"word": data_test[4], "position": 2}

        get_response = test_client.get("/api/v1/words")
        expected_response = (
            [data_test[0]] + [data_test[4]] + data_test[1:4] + data_test[5:]
        )
        assert get_response.status_code == 200
        assert get_response.json()["data"] == expected_response

    def test_patch_word_to_out_of_range_position(
        self,
        populate_mongo: None,
    ) -> None:
        response = test_client.patch(
            f"/api/v1/words/{data_test[4]}", json={"position": 50}
        )
        assert response.status_code == 200
        assert response.json() == {"word": data_test[4], "position": len(data_test)}

        get_response = test_client.get("/api/v1/words")
        expected_response = data_test[0:4] + data_test[5:] + [data_test[4]]
        assert get_response.status_code == 200
        assert get_response.json()["data"] == expected_response

    def test_patch_non_exising_word(
        self,
        populate_mongo: None,
    ) -> None:
        response = test_client.patch(
            "/api/v1/words/invented",
            json={"position": 2},
        )
        assert response.status_code == 404
        assert response.json()["message"] == "invented not found"
