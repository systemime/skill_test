import asyncio
import logging
import os

import aiohttp

# Create your views here.

session_list = {}
logger = logging.getLogger(__name__)


class Req:
    @property
    def set_session(self):
        try:
            loop = asyncio.get_running_loop()
        except:
            loop = asyncio.get_event_loop()
            asyncio.set_event_loop(loop)
        session = aiohttp.ClientSession(loop=loop)
        session_list[os.getpid()] = session
        return session

    def __init__(self):
        # loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        if session_list.get(os.getpid()):
            # logger.error(f"PID: {os.getpid()} 复用")
            self.session = session_list.get(os.getpid())
        else:
            logger.error(f"PID: {os.getpid()} 初次生成")
            self.session = self.set_session

    async def test(self):
        if session_list:
            session = session_list.get(os.getpid())
            if session and session.closed:
                session_list.pop(os.getpid())
                session = self.set_session
                print(f"[{os.getpid()}] session失效，重新生成，当前长度{len(session_list)}")
            elif not session:
                print(
                    f"[{os.getpid()}] 正常获取 session [{id(session)}], 当前长度{len(session_list)}"
                )
        else:
            print(f"[{os.getpid()}] session_list为空，创建一个session")
            session = self.set_session
            print(f"[{os.getpid()}] session_list长度为{len(session_list)}")

        if not session or not session.loop.is_running():
            session = self.set_session
            logger.warning(f"【异常 NoneType】-[{os.getpid()}] - len {len(session_list)}")
        # else:
        #     logger.error(f"PID: {os.getpid()} 复用")
        try:
            resp = await session.get("http://110.40.175.67:8090/get")
            return resp.status
        except Exception:
            return 500
        # async with session as ss:
        # # async with self.session as ss:
        #     cc = await ss.get("http://110.40.175.67:8090/get")
        #     # data = await cc.json()
        #     # print(data)


req = Req()
