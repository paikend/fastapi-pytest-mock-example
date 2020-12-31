from src.configs import INDEX_RESPONSE


def test_get_index_response(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.text == INDEX_RESPONSE
