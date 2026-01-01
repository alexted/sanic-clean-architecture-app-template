from sqlalchemy.sql import expression
from sqlalchemy.types import DateTime
from sqlalchemy.ext.compiler import compiles


class utcnow(expression.FunctionElement):
    type = DateTime()
    inherit_cache = True


@compiles(utcnow, "postgresql")
def pg_utcnow(element, compiler, **kw) -> str:  # noqa ANN001
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"
