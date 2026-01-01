from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.instrumentation.botocore import BotocoreInstrumentor
from opentelemetry.instrumentation.aiokafka import AIOKafkaInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor

from src.service.config import AppConfig


def setup_otel(config: AppConfig):
    provider = TracerProvider(
        resource=Resource.create({
            "service.name": config.APP_NAME,
            "service.namespace": "backend",
            "deployment.environment": config.ENVIRONMENT,
        })
    )
    trace.set_tracer_provider(provider)

    otlp_exporter = OTLPSpanExporter(endpoint=config.TELEMETRY_URL)

    span_processor = BatchSpanProcessor(otlp_exporter)
    provider.add_span_processor(span_processor)

    # Auto-instrumentation
    FastAPIInstrumentor().instrument()
    SQLAlchemyInstrumentor().instrument()
    RedisInstrumentor().instrument()
    BotocoreInstrumentor().instrument()
    AIOKafkaInstrumentor().instrument()
    HTTPXClientInstrumentor().instrument()
