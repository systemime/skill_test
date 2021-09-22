from functools import partial
from threading import Lock

import MySQLdb
from django.utils.itercompat import is_iterable
from sqlalchemy import event, exc
from sqlalchemy.pool import QueuePool


def _on_checkout(logger, pre_ping, dbapi_conn, *args):
    if pre_ping:
        try:
            dbapi_conn.ping(False)
            logger.debug("connect ping at %s success" % id(dbapi_conn))
        except MySQLdb.OperationalError as e:
            logger.debug("connect ping at %s fail, recreate connect" % id(dbapi_conn))
            raise exc.DisconnectionError(e)
    logger.debug("checkout at %s" % id(dbapi_conn))


def _on_checkin(logger, dbapi_conn, *args):
    logger.debug("checkin at %s" % id(dbapi_conn))


def _on_close(logger, dbapi_conn, *args):
    logger.debug("close at %s" % id(dbapi_conn))


def _on_connect(logger, dbapi_conn, *args):
    logger.debug("connect at %s" % id(dbapi_conn))


def _on_first_connect(logger, dbapi_conn, *args):
    logger.debug("first_connect at %s" % id(dbapi_conn))


class Pool:
    def __new__(
        cls,
        *,
        creator,
        pool_size=5,
        max_overflow=10,
        timeout=30,
        use_lifo=False,
        recycle=-1,
        logging_name=None
    ):
        """

        :param creator:
        :param pool_size: 连接池大小
        :param max_overflow: 连接池可溢出最大值
        :param timeout: 等待超时时间
        :param use_lifo: 是否后进先出
        :param recycle: 连接回收时间
        :param logging_name: 日志名称
        :param pre_ping: 是否每次校验连接有效
        """
        return QueuePool(
            creator,
            pool_size,
            max_overflow,
            timeout,
            use_lifo,
            recycle=recycle,
            logging_name=logging_name,
        )


class ConnPool:
    """
    没有使用sqlalchemy.pool的manage来实现，
    是考虑到可能针对不同数据库会采用不同的pool配置，所以更改了一下
    """

    def __init__(self):
        self.pool_map = {}
        self._create_pool_mutex = Lock()

    def __getattr__(self, item):
        return getattr(MySQLdb, item)

    def _serialize(self, value):
        """获取可hash对象，值相同即可，顺序可不一致"""
        if isinstance(value, dict):
            return frozenset(
                (key, self._serialize(nested_value))
                for key, nested_value in value.items()
            )
        try:
            hash(value)
        except TypeError:
            if is_iterable(value):
                return frozenset(map(self._serialize, value))
            # Non-hashable, non-iterable.
            raise
        return value

    @staticmethod
    def add_event(pool, logger, pre_ping):
        event.listen(pool, "checkout", partial(_on_checkout, logger, pre_ping))
        event.listen(pool, "checkin", partial(_on_checkin, logger))
        event.listen(pool, "close", partial(_on_close, logger))
        event.listen(pool, "connect", partial(_on_connect, logger))
        event.listen(pool, "first_connect", partial(_on_first_connect, logger))

    def get_pool(self, **conn_params):
        """conn_params 是数据库链接参数"""
        pool_options = conn_params.pop("POOL", {})
        """得到frozenset不可变列表元组对象"""
        key = self._serialize(conn_params)
        try:
            """获取pool链接参数"""
            return self.pool_map[key]
        except KeyError:
            with self._create_pool_mutex:
                if key in self.pool_map:
                    return self.pool_map[key]
                pre_ping = pool_options.pop("pre_ping", False)
                pool = self.pool_map[key] = Pool(
                    creator=partial(MySQLdb.connect, **conn_params), **pool_options
                )
                self.add_event(pool, pool.logger, pre_ping)
                return pool

    def connect(self, **conn_params):
        return self.get_pool(**conn_params).connect()


Database = ConnPool()
