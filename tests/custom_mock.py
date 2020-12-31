import fakeredis.aioredis
from aiobotocore.response import StreamingBody
from botocore.utils import lowercase_dict
from urllib3._collections import HTTPHeaderDict

from src.configs import settings


async def custom_convert_to_response_dict(http_response, operation_model):
    response_dict = {
        "headers": HTTPHeaderDict(lowercase_dict(http_response.headers)),
        "status_code": http_response.status_code,
        "context": {
            "operation_name": operation_model.name,
        },
    }
    if response_dict["status_code"] >= 300:
        response_dict[
            "body"
        ] = http_response.content  # modified but removed `await`
    elif operation_model.has_event_stream_output:
        response_dict["body"] = http_response.raw
    elif operation_model.has_streaming_output:
        length = response_dict["headers"].get("content-length")
        response_dict["body"] = StreamingBody(http_response.raw, length)
    else:
        response_dict["body"] = http_response.content
    return response_dict


async def custom_create_redis_pool(address):
    return await fakeredis.aioredis.create_redis_pool(encoding="utf-8")


class KafkaProducerMock:
    queue = []
    topic = settings.kafka_topic

    def produce(self, data):
        self.queue.append(data)

    def close(self):
        self.queue = []
