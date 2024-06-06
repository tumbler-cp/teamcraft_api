from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser, User
from urllib.parse import parse_qs


@database_sync_to_async
def get_user(token: str):
    try:
        tkn = Token.objects.get(key=token)
        return tkn.user
    except Token.DoesNotExist:
        return AnonymousUser()


class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query = parse_qs(scope['query_string'].decode())
        token_key = query.get('token', [None])[0]
        scope['user'] = await get_user(token_key) if token_key else AnonymousUser()
        return await super().__call__(scope, receive, send)
