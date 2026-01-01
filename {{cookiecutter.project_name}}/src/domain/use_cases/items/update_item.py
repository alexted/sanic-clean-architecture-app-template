from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel, NonNegativeInt

from src.data.items import ItemDTO, ItemRepository
from src.domain.use_cases.base import BaseUseCase


class ItemData(BaseModel):
    """ """

    name: str
    description: str
    price: NonNegativeInt


class UpdateItemRequest(BaseModel):
    """ """

    id: NonNegativeInt
    data: ItemData


class UpdateItemResponse(BaseModel):
    """ """

    id: NonNegativeInt
    name: str
    description: str
    price: NonNegativeInt


class UpdateItemUseCase(BaseUseCase):

    def __init__(self, item_repo: Annotated[ItemRepository, Depends(ItemRepository)]):
        self.item_repo: ItemRepository = item_repo

    async def execute(self, request_object: UpdateItemRequest) -> UpdateItemResponse:
        """

        :param request_object:
        :return:
        """
        item: ItemDTO = await self.item_repo.update(request_object.id, request_object.data)
        return UpdateItemResponse.construct(**item.dict())
