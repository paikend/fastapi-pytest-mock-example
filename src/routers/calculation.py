from fastapi import APIRouter, Request, status, HTTPException

from src.models.calculation import Add, CreateLogAdd
from src.utils.calculation import put_add_to_dynamodb
from src.utils.kafka import kafka_logging

router = APIRouter()


@router.post(
    "/add",
    tags=["logs"],
    status_code=status.HTTP_201_CREATED,
)
async def post_logs(request: Request, item: Add):
    redis = await request.app.state.redis
    is_succeed = await put_add_to_dynamodb(item.dict())
    if not is_succeed:
        return HTTPException(
            detail={"message": "ERROR: add is not created"}, status_code=500
        )
    kafka_logging(CreateLogAdd(**item.dict()))
    await redis.set("add", item.answer)
    return {"message": "add is created"}
