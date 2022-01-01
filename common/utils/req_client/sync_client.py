import logging

import httpx
from fake_useragent import UserAgent

logger = logging.getLogger(__name__)


class SyncClient:
    ua = UserAgent()

    def __int__(self, *args, **kwargs):
        mc = kwargs.get("max_connections", 50)
        mkc = kwargs.get("max_keepalive_connections", None)
        _time = kwargs.get("time_out", 10.0)
        timeout = httpx.Timeout(_time, connect=60.0)
        limits = httpx.Limits(max_connections=mc, max_keepalive_connections=mkc)
        self.client = httpx.Client(limits=limits, timeout=timeout)

    @property
    def header(self):
        return {
            "User-Agent": self.ua.random,
            "Accept": "*/*",
            "Connection": "keep-alive",
            "Accept-Language": "zh-CN,zh;q=0.8",
        }

    def send(self, url, method="GET", headers=None, params=None, data=None, json=None):

        headers = self.header if not headers else headers
        http_request = self.client.build_request(
            method=method, url=url, params=params, data=data, json=json, headers=headers
        )
        resp = self.client.send(http_request)
        return resp


client = SyncClient()
