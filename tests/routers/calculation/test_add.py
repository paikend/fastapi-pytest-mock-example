from src.utils.kafka import kafka_producer


def test_post_add_response(client, set_datetime, create_add_table_dynamodb):
    body = {"value_a": 3, "value_b": 10}
    response = client.post("/add", json=body)
    assert response.status_code == 201
    assert response.json() == {"message": "add is created"}
    assert len(kafka_producer._producer.queue) == 1
