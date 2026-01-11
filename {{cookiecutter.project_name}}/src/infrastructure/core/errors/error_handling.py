from datetime import UTC, datetime

from sanic import Request, json
import msgspec
from sanic.exceptions import SanicException

from ..log_config import CORRELATION_ID


async def sanic_error_handler(request: Request, exception: Exception):
    # Значения по умолчанию
    status_code = 500
    error_type = "INTERNAL_ERROR"
    message = str(exception)

    # 1. Ошибки самого Sanic (404, 405 и т.д.)
    if isinstance(exception, SanicException):
        status_code = exception.status_code
        error_type = "ROUTING_ERROR"

    # 2. Ошибки валидации msgspec (вместо Pydantic)
    elif isinstance(exception, msgspec.ValidationError):
        status_code = 422
        error_type = "VALIDATION_ERROR"
        # msgspec дает лаконичное описание ошибки
        message = f"Invalid input: {str(exception)}"

    # 3. Кастомные доменные ошибки (если есть)
    # elif isinstance(exception, MyDomainError): ...

    # Формируем DTO ответа
    payload = {
        "error": error_type,
        "message": message,
        # Достаем correlation_id из ContextVar или request.ctx
        "request_id": CORRELATION_ID.get() or getattr(request.ctx, "correlation_id", "unknown"),
        "timestamp": datetime.now(UTC).isoformat(),
    }

    return json(payload, status=status_code)
