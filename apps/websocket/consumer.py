import json
import logging

# unquote： 恢复url中被转义的部分，parse_qsl将url参数转为字典
from urllib.parse import parse_qsl, unquote

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer

from common.utils.websocket.handler import user_alert_push

# from autobutler_open.apps.account.models.user import User
# from autobutler_open.authentications import api_authentication
# from autobutler_open.websocket.message_push_handler import user_push, UserAlertPushHandler, user_alert_push


logger = logging.getLogger(__name__)


class AsyncUserOrdersConsumer(AsyncWebsocketConsumer):
    """用户通知"""

    async def connect(self):
        """建立连接"""

        self.group_name = user_alert_push.SINGLE_USER_GROUP_CHANNEL.format(
            uid=self.scope["user"].id
        )
        # from django_redis import get_redis_connection
        # con = get_redis_connection()
        # # 过期时间
        # con.ttl(f"asgi:group:{self.group_name}") / 3600
        # # 组元素合集
        # con.zrange(f"asgi:group:{self.group_name}", 0, -1)
        # # 向某频道发送
        # await self.channel_layer.send("channel_name", "message")
        # # 不知道干啥的玩意
        # # await self.channel_layer.router.channels
        # # 默认组过期时间
        await self.channel_layer.group_expiry
        # # 重新设置组过期时间并尊重分片(来自RedisChannelLayer)
        # # 从这里可以看出每次group_add都会再次更新过期时间为24小时
        # # 同时如果想直接操作 redis key，建议也使用如下上下文装饰器
        # group_key = self.channel_layer._group_key(self.group_name)
        # async with self.channel_layer.connection(self.channel_layer.consistent_hash(self.group_name)) as connection:
        #     # # Add to group sorted set with creation time as timestamp
        #     # await connection.zadd(group_key, time.time(), channel)
        #     # Set expiration to be group_expiry, since everything in
        #     # it at this point is guaranteed to expire before that
        #     await connection.expire(group_key, self.channel_layer.group_expiry)
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self.send(text_data="666")

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def close(self, code=None):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        await super().close()

    async def receive(self, text_data=None, bytes_data=None):

        user = self.scope["user"]
        # # 发送错误标记
        # await self.send(text_data=json.dumps({"error": True, "detail": "解析请求参数失败"}))

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "send_data",
                "message": f"{user.id} :: {user.username}",
            },
        )

    async def send_data(self, data):
        """发送数据"""
        await self.send(text_data=str(data))
