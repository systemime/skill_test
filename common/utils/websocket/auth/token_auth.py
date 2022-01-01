import logging
from typing import Union
from urllib import parse

# from autobutler_open.authentications import api_authentication
from channels.auth import AuthMiddlewareStack, UserLazyObject, get_user
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware

logger = logging.getLogger(__name__)


class TokenAuthMiddleware(BaseMiddleware):
    """
    websocket 连接token校验
    """

    @database_sync_to_async
    def _get_user(self, scope, token):
        try:
            # user = api_authentication(token)
            # TODO: 实现user获取方法
            user = None
            scope["user"] = user
        except Exception as err:
            logger.error(f"站内消息websocket认证失败，{err}")
            return False
        return True

    @staticmethod
    def get_token(scope: dict) -> Union[None, str]:

        if "user" not in scope:
            scope["user"] = UserLazyObject()

        headers = dict(scope["headers"])
        url_param = {}
        if scope["query_string"]:
            url_param = dict(parse.parse_qsl(scope["query_string"].decode()))

        token: Union[None, str] = None
        if b"authorization" in headers:
            token = headers[b"authorization"].decode()
        elif "authorization" in url_param:
            token = url_param.get("authorization")

        return token

    async def __call__(self, scope, receive, send):
        """
        仅判断token存在时进行校验
        """

        token = self.get_token(scope)

        token_verified = False
        if token:
            res = await self._get_user(scope, token)
            if res:
                token_verified = True

        scope["token_verified"] = token_verified

        return await self.inner(dict(scope), receive, send)


# Handy shortcut for applying all four layers at once
def TokenAuthMiddlewareStack(inner):
    return TokenAuthMiddleware(AuthMiddlewareStack(inner))
