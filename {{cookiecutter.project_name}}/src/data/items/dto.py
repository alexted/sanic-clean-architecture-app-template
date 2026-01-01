from pydantic import BaseModel


class ItemDTO(BaseModel):
    id: int
    name: str
    description: None | str
    price: float

    class Config:
        from_attributes = True


class ItemFilters(BaseModel):
    id: list[int]
