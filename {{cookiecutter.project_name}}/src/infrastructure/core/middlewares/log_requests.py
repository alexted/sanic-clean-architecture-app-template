from time import time
from sanic import Request, HTTPResponse
import logging

logger = logging.getLogger("sddfvwefve")


async def log_request_start(request: Request):
    if request.path not in ("/health", "/metrics"):
        request.ctx.start_time = time()


async def log_request_end(request: Request, response: HTTPResponse):
    if request.path in ("/health", "/metrics"):
        return

    duration = round(time() - getattr(request.ctx, "start_time", time()), 3)

    logger.info({
        "method": request.method,
        "resource": request.path,
        "query_params": dict(request.args),
        "correlation_id": getattr(request.ctx, "correlation_id", None),
        "response_status": response.status,
        "execution_duration": duration,
        # Для логирования body в Sanic:
        # request.body и response.body доступны напрямую
    })