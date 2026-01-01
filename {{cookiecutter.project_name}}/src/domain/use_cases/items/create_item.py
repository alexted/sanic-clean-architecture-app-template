from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel, NonNegativeInt

from src.data.items import ItemDTO, ItemRepository
from src.domain.use_cases.base import BaseUseCase


class CreateItemRequest(BaseModel):
    """ """

    name: str
    description: str
    price: NonNegativeInt


class CreateItemResponse(BaseModel):
    """ """

    id: NonNegativeInt
    name: str
    description: str
    price: NonNegativeInt


class CreateItemUseCase(BaseUseCase):

    def __init__(self, item_repo: Annotated[ItemRepository, Depends(ItemRepository)]):
        self.item_repo: ItemRepository = item_repo

    async def execute(self, request_object: CreateItemRequest) -> CreateItemResponse:
        """

        :param request_object:
        :return:
        """
        item: ItemDTO = await self.item_repo.create(request_object)
        return CreateItemResponse.construct(**item.dict())
