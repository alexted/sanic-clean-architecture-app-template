from opentelemetry.instrumentation.asgi import OpenTelemetryMiddleware
from sanic import Sanic, response
from sanic_ext import Extend
import sentry_sdk
from sanic_prometheus import monitor

from src.api import v1_blueprint

from .settings import AppConfig, EnvironmentEnum, get_config
from .telemetry import setup_otel
from .log_config import init_logging
from .middlewares.log_requests import log_request_end, log_request_start
from .middlewares.correlation_id import handle_correlation_id_request, handle_correlation_id_response
from .errors.error_handling import sanic_error_handler


def create_app() -> Sanic:
    config: AppConfig = get_config()
    init_logging(config)

    app = Sanic(config.APP_NAME)

    app.config.update(OAS_URL_PREFIX="/docs", OAS_UI_DEFAULT="swagger")

    Extend(
        app,
        config={
            "oas": {
                "info": {
                    "title": config.APP_NAME,
                    "version": "1.0.0",
                    "description": "...",
                    "license": {"name": "Proprietary Software License"},
                }
            }
        },
    )

    # Health check
    @app.get("/health")
    async def health_check(request):
        return response.empty(status=200)

    # todo Здесь скорее всего надо использовать
    #  app.error_handler = CustomErrorHandler()
    #  вместо обработки конкретных исключений (хоть и с широкой маской `Exception`):
    app.error_handler.add(Exception, sanic_error_handler)

    # todo сюда надо добавить аутентификацию
    app.register_middleware(handle_correlation_id_request, "request")
    app.register_middleware(log_request_start, "request")
    app.register_middleware(handle_correlation_id_response, "response")
    app.register_middleware(log_request_end, "response")

    setup_otel(config)
    # app = OpenTelemetryMiddleware(app)

    if config.ENVIRONMENT == EnvironmentEnum.PROD:
        sentry_sdk.init(dsn=config.SENTRY_URL, traces_sample_rate=1.0)
        monitor(app).expose_endpoint()

    app.blueprint(v1_blueprint)

    # todo сюда
    from src.domain.use_cases.numbers import DivideUseCase, MultiplyUseCase, SubtractUseCase, SummariseUseCase

    app.ext.dependency(SummariseUseCase)
    app.ext.dependency(SubtractUseCase)
    app.ext.dependency(MultiplyUseCase)
    app.ext.dependency(DivideUseCase)
    # И так для всех UseCase и их зависимостей (Repository и т.д.)

    from src.domain.use_cases.items import GetItemUseCase, CreateItemUseCase, DeleteItemUseCase, UpdateItemUseCase

    # Sanic попробует создать их без аргументов, если в __init__ ничего нет,
    # или инжектить зависимости в них рекурсивно, если сабзависимости предварительно были так же зарегистрированы (вся цепочка).
    app.ext.dependency(CreateItemUseCase)
    app.ext.dependency(GetItemUseCase)
    app.ext.dependency(UpdateItemUseCase)
    app.ext.dependency(DeleteItemUseCase)

    return app
