import msgspec
from functools import wraps
from sanic import Request, json, Sanic
from sanic.ext import validate
from sanic_ext.extensions.openapi import definition


# 1. Хелпер для конвертации msgspec в JSON-схему (для Swagger)
def msgspec_to_openapi(struct_cls: type[msgspec.Struct]):
    # msgspec умеет генерировать JSON-схему сам!
    schema, _ = msgspec.json.schema_components([struct_cls], str)
    return schema[struct_cls.__name__]


# 2. Наш универсальный декоратор
def docs_msgspec(json_model: type[msgspec.Struct]):
    def decorator(f):
        # Регистрируем схему в OpenAPI Sanic
        # Мы говорим Sanic: "Для этого роута в теле запроса ожидай вот такую схему"
        schema = msgspec_to_openapi(json_model)

        # Оборачиваем функцию для Swagger
        f_with_docs = definition(body={"application/json": schema})(f)

        @wraps(f)
        async def decorated_function(request: Request, *args, **kwargs):
            try:
                # Валидация msgspec (самая быстрая часть)
                data = msgspec.json.decode(request.body, type=json_model)
            except msgspec.ValidationError as e:
                return json({"error": "Validation Failed", "details": str(e)}, status=422)

            # Прокидываем валидированный объект в функцию как 'data'
            return await f_with_docs(request, data, *args, **kwargs)

        return decorated_function

    return decorator


# --- ПРИМЕР ИСПОЛЬЗОВАНИЯ ---

class UserProfile(msgspec.Struct):
    username: str
    age: int
    bio: str | None = None


app = Sanic("ExpertSanicApp")


@app.post("/user")
@docs_msgspec(UserProfile)  # И валидация, и дока в одном флаконе
async def create_user(request: Request, data: UserProfile):
    # 'data' здесь — это уже готовый объект UserProfile
    return json({"received": data.username, "age": data.age})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, dev=True)