from sanic import Blueprint
from src.api.items import bp as items_bp
from src.api.numbers import bp as numbers_bp # Предполагаем, что там тоже заменили

# Создаем группу (эквивалент include_router с префиксом)
v1_blueprint = Blueprint.group(items_bp, numbers_bp, url_prefix="/v1")

__all__ = ("v1_blueprint",)