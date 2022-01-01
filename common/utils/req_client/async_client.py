"""
to_async
"""
import asyncio
import logging
import os
import sys
import warnings

import aiohttp
from aiohttp_proxy import ProxyConnector, ProxyType
from fake_useragent import UserAgent

session_list = {}
logger = logging.getLogger(__name__)


class AsyncClient:
    @property
    def proxy(self):
        """
        获取一个代理
        http://user:password@127.0.0.1:1080
        """
        return

    def __init__(self, **kwargs):
        self.ua = UserAgent()  # 不支持多进程
        if session_list.get(os.getpid()):
            self.session = session_list.get(os.getpid())
        else:
            self.session = self.set_session(**kwargs)

    def set_session(self, use_proxy=False, proxy=None, **kwargs):
        try:
            loop = asyncio.get_running_loop()
        except Exception as e:
            logger.exception(
                "===>> local thread no running event loop, set new loop <<===",
                exc_info=e,
            )
            loop = asyncio.get_event_loop()
            asyncio.set_event_loop(loop)

        param = {"loop": loop}

        if use_proxy and proxy:
            conn = ProxyConnector.from_url(proxy)
            param.update({"connector": conn})

        session = aiohttp.ClientSession(**param)
        if kwargs.get("is_celery"):
            session_list[(os.getpid(), "celery")] = session
        else:
            session_list[os.getpid()] = session
        return session

    @property
    def header(self):
        return {
            "User-Agent": self.ua.random,
            "Accept": "*/*",
            "Connection": "keep-alive",
            "Accept-Language": "zh-CN,zh;q=0.8",
        }

    @property
    def refresh(self):
        """重新生成session"""
        session = self.set_session()
        return session

    async def get_session(self, **kwargs):
        if session_list:
            if kwargs.get("is_celery"):
                session = session_list.get((os.getpid(), "celery"))
            else:
                session = session_list.get(os.getpid())
            if session and session.closed:
                session_list.pop(os.getpid())
                session = self.set_session(**kwargs)
            elif not session:
                session = self.set_session(**kwargs)
        else:
            session = self.set_session(**kwargs)

        if not session:
            logger.exception(ModuleNotFoundError("session 意外丢失"))
            sys.exit()
        if not session.loop.is_running():
            logger.warning(
                f"【事件循环异常】- [{os.getpid()}] - "
                f"重置当前线程 loop 及 aiohttp client session - "
                f"当前session数量 {len(session_list)}"
            )
            session = self.set_session(**kwargs)

        return session

    async def get(self, url, **kwargs):
        """
        kwargs: header=None, proxy=None
        PS: 建议请求头、代理在请求时加入，不要直接放到session上，否则无法更改，同时代理可能失效
        http://110.40.175.67:8090/get
        """
        timeout = kwargs.pop("timeout", 10)
        session = await self.get_session(**kwargs)
        if kwargs.get("delay", 0) > 0:
            await asyncio.sleep(kwargs.pop("delay"))

        try:
            if not kwargs.get("headers") and not kwargs.pop("not_headers", False):
                kwargs.update({"headers": self.header})
            for field in ("is_celery", "use_proxy", "proxy"):
                kwargs.pop(field, None)
            resp = await session.get(url, timeout=timeout, **kwargs)
            return resp
        except Exception as e:
            logger.exception(e)
            return None


client = AsyncClient()
