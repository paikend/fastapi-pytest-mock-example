from datetime import datetime
import uuid
from typing import Optional

from pydantic import BaseModel, validator
from pytz import timezone


class Add(BaseModel):
    id: str = None
    value_a: int
    value_b: int
    answer: int = None
    created: Optional[str] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.answer = self.value_a + self.value_b

    @validator("id", always=True)
    def set_id(cls, v):
        if v is None:
            return str(uuid.uuid4())

    @validator("created", always=True)
    def set_created(cls, v):
        if v:
            return
        return datetime.now(tz=timezone("Asia/Seoul")).isoformat(sep="T")


class CreateLogAdd(Add):
    action: str = "CreateAddLog"
    requested: Optional[str] = None

    @validator("requested", always=True)
    def set_requested(cls, v):
        if v:
            return
        return datetime.now(tz=timezone("Asia/Seoul")).isoformat(sep="T")
