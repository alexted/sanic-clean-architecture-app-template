import logging

from pydantic import BaseModel

from src.domain.use_cases.base import BaseUseCase

logger = logging.getLogger()


class SummariseRequest(BaseModel):
    x: int
    y: int


class SummariseResponse(BaseModel):
    sum: int


class SummariseUseCase(BaseUseCase):

    async def execute(self, request_object: SummariseRequest) -> SummariseResponse:
        logger.info("test message")
        return SummariseResponse(sum=request_object.x + request_object.y)
