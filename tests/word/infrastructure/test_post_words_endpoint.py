from tests.conftest import data_test, test_client


class TestPostWordsEndpoint:
    def test_post_word_at_beggining(self, populate_mongo: None) -> None:
        post_response = test_client.post(
            "/api/v1/words", json={"word": "botella", "position": 1}
        )

        assert post_response.status_code == 201
        assert post_response.json() == {"word": "botella", "position": 1}
        response = test_client.get("/api/v1/words")
        expected_response = ["botella"] + data_test

        assert response.status_code == 200
        assert response.json()["data"] == expected_response

    def test_post_word_in_the_middle(
        self,
        populate_mongo: None,
    ) -> None:
        post_response = test_client.post(
            "/api/v1/words", json={"word": "botella", "position": 4}
        )
        assert post_response.status_code == 201
        assert post_response.json() == {"word": "botella", "position": 4}
        response = test_client.get("/api/v1/words")
        expected_response = data_test[0:3] + ["botella"] + data_test[3:]
        assert response.status_code == 200
        assert response.json()["data"] == expected_response

    def test_post_word_out_of_the_range(
        self,
        populate_mongo: None,
    ) -> None:
        post_response = test_client.post(
            "/api/v1/words", json={"word": "botella", "position": 25}
        )
        assert post_response.status_code == 201
        assert post_response.json() == {
            "word": "botella",
            "position": len(data_test) + 1,
        }
        response = test_client.get("/api/v1/words")
        expected_response = data_test + ["botella"]
        assert response.status_code == 200
        assert response.json()["data"] == expected_response

    def test_post_already_existing_word(
        self,
        populate_mongo: None,
    ) -> None:
        post_response = test_client.post(
            "/api/v1/words", json={"word": data_test[2], "position": 25}
        )
        assert post_response.status_code == 409
        assert post_response.json()["message"] == f"{data_test[2]} already exists"
        response = test_client.get("/api/v1/words")
        expected_response = data_test
        assert response.status_code == 200
        assert response.json()["data"] == expected_response

    def test_post_two_words(
        self,
        populate_mongo: None,
    ) -> None:
        post_response = test_client.post(
            "/api/v1/words", json={"word": "dos palabras", "position": 25}
        )
        assert post_response.status_code == 403
        assert post_response.json()["message"] == f"Word does not follow the pattern"
        response = test_client.get("/api/v1/words")
        expected_response = data_test
        print(response.json())
        assert response.status_code == 200
        assert response.json()["data"] == expected_response
