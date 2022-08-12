from tests.conftest import data_test, test_client


class TestPatchWordsEndpoint:

    def test_patch_word_to_higher_position(self) -> None:
        response = test_client.patch(f"/api/v1/words/{data_test[2]}", json={"position": 5})
        assert response.status_code == 200
        assert response.json() == {"word": data_test[2], "position": 5}

        get_response = test_client.get("/api/v1/words")
        expected_response = data_test[0:2] + data_test[3:5] + [data_test[2]] + data_test[5:]
        get_response == 200
        get_response.json()["data"] == expected_response