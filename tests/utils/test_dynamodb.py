import pytest
from starlette import status

from src.configs import settings
from src.models.calculation import Add
from src.utils.dynamodb import put_to_dynamodb


@pytest.mark.asyncio
async def test_put_to_dynamodb_status_ok(create_add_table_dynamodb):
    item = Add(value_a=5, value_b=3)
    response = await put_to_dynamodb(
        item.dict(), settings.dynamodb_add_table_name
    )
    assert response["ResponseMetadata"]["HTTPStatusCode"] == status.HTTP_200_OK
