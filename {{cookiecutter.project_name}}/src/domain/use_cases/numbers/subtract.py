import logging

from pydantic import BaseModel

from src.domain.use_cases.base import BaseUseCase

logger = logging.getLogger()


class SubtractRequest(BaseModel):
    left_number: int
    right_number: int


class SubtractResponse(BaseModel):
    result: int


class SubtractUseCase(BaseUseCase):

    async def execute(self, request_object: SubtractRequest) -> SubtractResponse:
        logger.info("test message")
        return SubtractResponse(result=request_object.left_number - request_object.right_number)
