from collections.abc import Iterator, AsyncIterator, AsyncGenerator

from httpx import AsyncClient, ASGITransport
import pytest
from fastapi import FastAPI
from filelock import FileLock
from sqlalchemy import NullPool
from alembic.config import Config as AlembicConfig
from alembic.command import upgrade, downgrade
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

{% if cookiecutter.use_postgresql | lower == 'y' -%}
from tests.data import mock_data
{% endif -%}
from src.infrastructure.core.settings import get_config
from src.infrastructure.core.application import create_app
{% if cookiecutter.use_postgresql | lower == 'y' -%}
from src.infrastructure.clients.postgres.engine import get_db_session
{% endif %}

TEST_APP_URL = "http://test"

pytest_plugins = ("tests.fixtures.items",)


@pytest.fixture(scope="module")
def anyio_backend() -> str:
    """
    # Required per https://anyio.readthedocs.io/en/stable/testing.html#using-async-fixtures-with-higher-scopes
    """
    return "asyncio"


{%- if cookiecutter.use_postgresql|lower == 'y' %}
@pytest.fixture(scope="session", autouse=True)
def migrations(tmp_path_factory) -> None:
    alembic_config = AlembicConfig("alembic.ini")
    alembic_config.attributes["configure_logger"] = False

    root_tmp_dir = tmp_path_factory.getbasetemp().parent

    fn = root_tmp_dir / "data.json"
    with FileLock(str(fn) + ".lock"):
        upgrade(alembic_config, "head")
        yield "on head"
        downgrade(alembic_config, "base")


@pytest.fixture(scope="session")
def db_engine() -> AsyncEngine:
    return create_async_engine(get_config().POSTGRES_DSN.unicode_string(), poolclass=NullPool)


@pytest.fixture(autouse=True)
async def db_session(db_engine: AsyncEngine) -> AsyncIterator[AsyncSession]:
    """
    Create a transactional test database session.
    https://docs.sqlalchemy.org/en/latest/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites
    """
    # expose session
    async with async_sessionmaker(db_engine, expire_on_commit=False).begin() as session:
        try:
            yield session
        finally:
            await session.rollback()
{% endif -%}


@pytest.fixture
def app({% if cookiecutter.use_postgresql|lower == 'y' -%}migrations: None, db_session: AsyncSession{% endif -%}) -> FastAPI:
    app_instance = create_app()

    {%- if cookiecutter.use_postgresql | lower == 'y' %}
    def get_db_session_override() -> Iterator[AsyncSession]:
        try:
            yield db_session
        finally:
            pass

    app_instance.dependency_overrides[get_db_session] = get_db_session_override
    {% endif %}
    return app_instance


@pytest.fixture()
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient]:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url=TEST_APP_URL,
        {% if cookiecutter.use_jwt | lower == 'y' %}
        headers={"Authorization": f"Bearer {mock_data.items[0]['id']}"},
        {% endif %}
    ) as client:
        yield client
