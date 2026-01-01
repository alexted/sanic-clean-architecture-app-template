from sanic import json, Request
from sanic.exceptions import SanicException, NotFound
from pydantic import ValidationError

async def sanic_error_handler(request: Request, exception: Exception):
    status_code = 500
    error_type = "INTERNAL_ERROR"
    message = str(exception)

    if isinstance(exception, SanicException):
        status_code = exception.status_code
    elif isinstance(exception, ValidationError):
        status_code = 422
        error_type = "VALIDATION_ERROR"
        message = exception.errors()
    # Добавьте проверку на ваш OtherError

    return json({
        "error": error_type,
        "message": message,
        "correlation_id": getattr(request.ctx, "correlation_id", None),
        "timestamp": datetime.now(UTC).isoformat()
    }, status=status_code)
