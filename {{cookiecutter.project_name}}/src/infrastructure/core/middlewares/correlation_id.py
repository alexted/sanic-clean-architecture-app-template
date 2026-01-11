from uuid import uuid4
from contextvars import ContextVar

from sanic import Request, HTTPResponse

CORRELATION_ID: ContextVar[str | None] = ContextVar("correlation_id", default=None)


# request middleware
async def handle_correlation_id_request(request: Request) -> None:
    correlation_id = request.headers.get("X-Request-ID", str(uuid4()))
    request.ctx.correlation_id = correlation_id  # В Sanic используем .ctx вместо .state
    CORRELATION_ID.set(correlation_id)

    # Sentry extension вызывается здесь
    # sentry_extension(correlation_id)


# response middleware
async def handle_correlation_id_response(request: Request, response: HTTPResponse) -> None:
    correlation_id = getattr(request.ctx, "correlation_id", None)
    if correlation_id:
        response.headers["X-Request-ID"] = correlation_id
    CORRELATION_ID.set(None)
