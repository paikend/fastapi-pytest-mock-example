from typing import Dict

import aioboto3


async def put_to_dynamodb(item: Dict, table_name: str) -> Dict:
    async with aioboto3.resource("dynamodb", verify=False) as dynamo_resource:
        table = await dynamo_resource.Table(table_name)
        response = await table.put_item(Item=item)
    return response
