import logging

from pydantic import BaseModel

from src.domain.use_cases.base import BaseUseCase

logger = logging.getLogger()


class DivideRequest(BaseModel):
    dividend: int
    divisor: int


class DivideResponse(BaseModel):
    result: float


class DivideUseCase(BaseUseCase):

    async def execute(self, request_object: DivideRequest) -> DivideResponse:
        logger.info("test message")
        return DivideResponse(result=request_object.dividend / request_object.divisor)
