from typing import Dict

from starlette import status

from src.configs import settings
from src.utils.dynamodb import put_to_dynamodb


async def put_add_to_dynamodb(item: Dict):
    response = await put_to_dynamodb(item, settings.dynamodb_add_table_name)
    return response["ResponseMetadata"]["HTTPStatusCode"] == status.HTTP_200_OK
