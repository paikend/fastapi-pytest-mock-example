from datetime import datetime

import boto3
import pytest
from fastapi.testclient import TestClient
from moto import mock_dynamodb2
from pytz import timezone

from src.configs import settings
from src.configs.base import app
from tests.custom_mock import KafkaProducerMock
from src.utils.redis import redis


@pytest.fixture(autouse=True)
def set_kafka_producer(mocker):
    def produce(self, data):
        self._producer.produce(data)

    def close(self):
        self._producer.close()

    mocker.patch(
        "src.utils.kafka.KafkaProducer._producer", KafkaProducerMock()
    )
    mocker.patch("src.utils.kafka.KafkaProducer.produce", produce)
    mocker.patch("src.utils.kafka.KafkaProducer.close", close)


@pytest.mark.asyncio
@pytest.fixture(autouse=True)
async def set_aiobotocore_endpoint_convert_to_response_dict(mocker):
    from tests.custom_mock import custom_convert_to_response_dict
    from aiobotocore import endpoint

    mocker.patch.object(
        endpoint,
        "convert_to_response_dict",
        custom_convert_to_response_dict,
    )


@pytest.mark.asyncio
@pytest.fixture(autouse=True)
async def set_aioredis(mocker):
    import aioredis
    from tests.custom_mock import custom_create_redis_pool

    mocker.patch.object(
        aioredis, "create_redis_pool", custom_create_redis_pool
    )

    con = await redis.create()
    yield
    con.close()
    await con.wait_closed()


@pytest.fixture
def set_datetime(freezer):
    freezer.move_to(
        datetime(2020, 11, 11, 5, 10, tzinfo=timezone("Asia/Seoul"))
    )


@pytest.fixture
def dynamodb():
    with mock_dynamodb2():
        yield


@pytest.fixture
def dynamodb_resource(dynamodb):
    yield boto3.resource("dynamodb")


@pytest.fixture
def create_add_table_dynamodb(dynamodb_resource):
    dynamodb_resource.create_table(
        TableName=settings.dynamodb_add_table_name,
        KeySchema=[
            {"AttributeName": "id", "KeyType": "HASH"},
            {"AttributeName": "created", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "id", "AttributeType": "S"},
            {"AttributeName": "created", "AttributeType": "S"},
        ],
    )


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client
