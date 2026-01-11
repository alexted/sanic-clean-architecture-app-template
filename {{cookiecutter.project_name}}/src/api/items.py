from sanic import Blueprint, Request, response
from sanic_ext import validate


# Импорты DTO и UseCases остаются теми же
from src.domain.use_cases.items import (
    GetItemRequest,
    GetItemResponse,
    GetItemUseCase,
    CreateItemRequest,
    CreateItemResponse,
    CreateItemUseCase,
    DeleteItemRequest,
    DeleteItemUseCase,
    UpdateItemRequest,
    UpdateItemResponse,
    UpdateItemUseCase
)

# Создаем Blueprint вместо APIRouter
bp = Blueprint("items", url_prefix="/items")


@bp.post("/")  # В Sanic url_prefix уже содержит /items, поэтому тут корень
async def create_item(
        request: Request,
        item_request: CreateItemRequest,  # Sanic-ext распарсит body в эту модель
        use_case: CreateItemUseCase  # Sanic-ext внедрит зависимость
) -> CreateItemResponse:
    """
    Create item
    """
    # Важно: если ваши UseCase асинхронные, убедитесь что DI их правильно создает.
    # Sanic-ext вернет объект Pydantic или dataclass.

    # Если execute возвращает Pydantic модель, Sanic-ext (v23+) может сам сериализовать её,
    # если использовать @openapi.definition или настроить сериализатор.
    # Но для надежности часто делают явный .model_dump() или используют json()

    result = await use_case.execute(item_request)
    return response.json(result.model_dump(), status=201)


@bp.get("/<item_id:int>")  # Синтаксис параметров пути в Sanic
async def get_item(
        request: Request,
        item_id: int,
        use_case: GetItemUseCase
) -> GetItemResponse:
    """
    Get item by id
    """
    # Валидация item_id как NonNegativeInt внутри роута сложнее чем в FastAPI,
    # обычно это делают внутри UseCase или Pydantic DTO.

    request_object = GetItemRequest(id=item_id)
    item = await use_case.execute(request_object)
    return response.json(item.model_dump())


@bp.put("/<item_id:int>")
async def update_item(
        request: Request,
        item_id: int,
        item_body: UpdateItemRequest,  # Body
        use_case: UpdateItemUseCase
) -> UpdateItemResponse:
    """
    Update item
    """
    # UpdateItemRequest скорее всего не содержит id в body, если это REST.
    # Возможно, придется "обогатить" модель id из пути.
    # item_body.id = item_id

    result = await use_case.execute(item_body)
    return response.json(result.model_dump())


@bp.delete("/<item_id:int>")
async def delete_item(
        request: Request,
        item_id: int,
        use_case: DeleteItemUseCase
):
    """
    Delete item
    """
    request_object = DeleteItemRequest(id=item_id)
    await use_case.execute(request_object)
    return response.empty(status=204)