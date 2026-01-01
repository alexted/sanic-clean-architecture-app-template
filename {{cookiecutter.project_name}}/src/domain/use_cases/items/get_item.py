from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel, NonNegativeInt

from src.data.items import ItemDTO, ItemRepository, ItemFilters
from src.domain.use_cases.base import BaseUseCase


class GetItemRequest(BaseModel):
    """ """

    id: NonNegativeInt


class GetItemResponse(BaseModel):
    """ """

    id: NonNegativeInt
    name: str
    description: str
    price: NonNegativeInt


class GetItemUseCase(BaseUseCase):

    def __init__(self, item_repo: Annotated[ItemRepository, Depends(ItemRepository)]):
        self.item_repo: ItemRepository = item_repo

    async def execute(self, request_object: GetItemRequest) -> GetItemResponse:
        """

        :param request_object:
        :return:
        """
        item: list[ItemDTO] = await self.item_repo.get(ItemFilters(id=[request_object.id]))
        return GetItemResponse.model_construct(**item[0].model_dump())
