from sanic import Sanic, Request, response
from sanic.response import json
from sanic.exceptions import SanicException
import sentry_sdk
from sanic_ext import Extend

# Ваши импорты (пути могут требовать корректировки внутри модулей)
from src.api import v1_blueprint  # переименовали v1_routes в v1_blueprint
from .settings import AppConfig, EnvironmentEnum, get_config
from .log_config import init_logging
# from .telemetry import fsetup_otel
from .middlewares.error_handling import sanic_error_handler
from .middlewares.correlation_id import handle_correlation_id_request, handle_correlation_id_response
from .middlewares.log_requests import log_request_start, log_request_end

# Middleware и ExceptionHandler придется адаптировать (см. ниже)

def create_app() -> Sanic:
    config: AppConfig = get_config()
    init_logging(config)

    # Инициализация Sanic
    app = Sanic(config.APP_NAME)

    # Конфигурация Sanic (можно передать dict)
    app.config.update(
        OAS_URL_PREFIX="/docs",  # Swagger UI
        OAS_UI_DEFAULT="swagger",
    )

    # Подключение sanic-ext (OpenAPI, Injection, Validation)
    # Настраиваем информацию для Swagger
    Extend(app, config={
        "oas": {
            "info": {
                "title": config.APP_NAME,
                "version": "1.0.0",
                "description": "...",
                "license": {"name": "Proprietary Software License"}
            }
        }
    })

    # Регистрация ошибок
    app.error_handler.add(Exception, sanic_error_handler)

    # Регистрация middleware
    app.register_middleware(handle_correlation_id_request, "request")
    app.register_middleware(log_request_start, "request")
    app.register_middleware(handle_correlation_id_response, "response")
    app.register_middleware(log_request_end, "response")

    # setup_otel(config)

    if config.ENVIRONMENT == EnvironmentEnum.PROD:
        sentry_sdk.init(dsn=config.SENTRY_URL, traces_sample_rate=1.0)
        # Для Prometheus в Sanic обычно используют sanic-prometheus или кастомный endpoint

    # Health check
    @app.get("/health")
    async def health_check(request):
        return response.empty(status=200)

    # Подключение роутов (Blueprints)
    app.blueprint(v1_blueprint)

    # --- Dependency Injection Registration ---
    # КРИТИЧЕСКИЙ МОМЕНТ:
    # В FastAPI Depends() создает экземпляр на лету.
    # В Sanic-ext мы регистрируем классы, чтобы он знал, как их инжектить.
    # Нам нужно зарегистрировать UseCases.

    # Регистрация DI (через sanic-ext)
    from src.domain.use_cases.numbers import SummariseUseCase
    app.ext.dependency(SummariseUseCase)
    # И так для всех UseCase и их зависимостей (Repository и т.д.)

    from src.domain.use_cases.items import (
        CreateItemUseCase, GetItemUseCase, UpdateItemUseCase, DeleteItemUseCase
    )
    # Sanic попробует создать их без аргументов, если в __init__ ничего нет,
    # или инжектить зависимости в них рекурсивно.
    app.ext.dependency(CreateItemUseCase)
    app.ext.dependency(GetItemUseCase)
    app.ext.dependency(UpdateItemUseCase)
    app.ext.dependency(DeleteItemUseCase)

    return app
