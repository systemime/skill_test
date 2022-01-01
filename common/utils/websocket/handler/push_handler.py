"""消息推送工具"""

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.cache import cache
from django_redis import get_redis_connection
from redis.exceptions import RedisError


class MessagePushHandler:
    """消息推送工具"""

    # TODO: 具体方法需要调整
    CONSUMER_CACHE_KEY = ""

    # 子类需定义USER_MESSAGE_PUSH_REGISTER_KEY 类属性

    def get_cache_key(self, user_id):
        """获取redis数据保存的key"""
        return f"{self.USER_MESSAGE_PUSH_REGISTER_KEY}::{user_id}"

    @staticmethod
    def push_message(channel_name, data):
        """向特定的channel_name发送消息推送"""
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.send)(
            channel_name, {"type": "send_data", "data": data}
        )

    @staticmethod
    def push_message_to_group(group_name, data):
        """向特定的组广播消息"""
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            group_name, {"type": "send_message", "message": data}
        )


class UserAlertMsgPushHandler(MessagePushHandler):

    # 将同一个用户开启多个标签页存放到同一个组管理
    SINGLE_USER_GROUP_CHANNEL = "USER_ORDER_ALERT_MSG_{uid}"


user_alert_push = UserAlertMsgPushHandler()


def consistency_check(*args, **kwargs):
    def inner(func):
        return

    return inner


class UserAlertPushHandler(MessagePushHandler):
    """用户头像处消息提醒工具类"""

    # 用户头像处消息推送-键名
    USER_MESSAGE_PUSH_REGISTER_KEY = "USER_ORDER_STATUS_ALERT_MSG_KEY"

    r_conn = get_redis_connection()

    def _registe_user_message_alert(self, user_id, channel_name):
        """注册用户的消息提醒"""
        register_key = self.get_cache_key(user_id)
        redis_pip = self.r_conn.pipeline()
        # 默认保存 24 小时
        redis_pip.watch(register_key, channel_name)
        redis_pip.multi()
        redis_pip.sadd(register_key, channel_name)
        redis_pip.expire(register_key, 3600 * 24)
        redis_pip.setex(channel_name, 24 * 3600, register_key)
        redis_pip.execute()

    def registe_user_message_alert(self, user_id, channel_name):
        try:
            self._registe_user_message_alert(user_id, channel_name)
        except RedisError as err:
            pass

    def unregiste_channel_name(self, channel_name):
        """删除用户的消息提醒事件"""
        register_key = self.r_conn.get(channel_name)
        if register_key:
            self.r_conn.srem(register_key, channel_name)
            self.r_conn.delete(channel_name)

    def get_user_push_channel_name(self, user_id, push_typ=None):  # pylint: disable=all
        """判断是否需要向目标用户的特定消息类型发送推送"""
        register_key = self.get_cache_key(user_id)
        all_channels = self.r_conn.smembers(register_key)
        all_channels = [item.decode() for item in all_channels]
        return all_channels


user_push = UserAlertPushHandler()
