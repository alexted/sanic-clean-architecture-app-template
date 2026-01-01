from functools import wraps
from sanic import exceptions


def protected():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            token = request.headers.get("Authorization")
            if not token:
                raise exceptions.Unauthorized("Missing token")

            # Логика проверки токена через IDPService
            # Можно достать idp_client из app.ctx или через DI
            user_info = await request.app.ctx.idp_client.get_user_info(token)

            if not user_info:
                raise exceptions.Unauthorized("Invalid token")

            request.ctx.user = user_info
            return await f(request, *args, **kwargs)

        return decorated_function

    return decorator