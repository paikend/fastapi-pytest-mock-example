from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from src.configs import settings, INDEX_RESPONSE
from src.middlewares.base import attach_base_middleware
from src.utils.redis import redis
from src.utils.kafka import kafka_producer
from src.routers import calculation


app = FastAPI(redoc_url=settings.redoc_path, docs_url=settings.docs_path)
app = attach_base_middleware(app)
app.include_router(calculation.router)


@app.on_event("startup")
async def startup_event():
    app.state.redis = await redis.create()


@app.on_event("shutdown")
async def shutdown_event():
    app.state.redis.close()
    kafka_producer.close()
    await app.state.redis.wait_closed()


@app.get("/", response_class=PlainTextResponse)
async def hello_big_pearl():
    """
    Hello big_pearl
    """
    return INDEX_RESPONSE
