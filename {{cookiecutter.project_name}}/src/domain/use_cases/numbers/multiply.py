import logging

from pydantic import BaseModel

from src.domain.use_cases.base import BaseUseCase

logger = logging.getLogger()


class MultiplyRequest(BaseModel):
    x: int
    y: int


class MultiplyResponse(BaseModel):
    result: int


class MultiplyUseCase(BaseUseCase):

    async def execute(self, request_object: MultiplyRequest) -> MultiplyResponse:
        logger.info("test message")
        return MultiplyResponse(result=request_object.x * request_object.y)
