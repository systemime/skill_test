import asyncio
import logging
import os
import random
import time

import aiohttp
from asgiref.sync import async_to_sync, sync_to_async
from django.http import HttpResponse
from django.shortcuts import render  # noqa
from django.utils.decorators import classonlymethod
from django.views.generic import View

from apps.share.tasks.tt import func as t_func
from apps.share.tasks.tt import func2 as t_func2

from .models import Country
from .req_test.client import req, session_list

logger = logging.getLogger(__name__)


def func():
    cc: Country = Country.objects.last()
    cc.is_remove = False
    cc.save()


class TTT(View):
    @classonlymethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        view._is_coroutine = asyncio.coroutines._is_coroutine
        return view

    async def get(self, request):

        # await sync_to_async(func)()
        # is_running_loop = False
        # is_event_loop = False
        # try:
        #     is_running_loop = True
        #     loop = asyncio.get_running_loop()
        # except Exception:
        #     try:
        #         is_event_loop = True
        #         loop = asyncio.get_event_loop()
        #     except:
        #         pass
        #
        # print("===", loop, "is_running_loop", is_running_loop, "is_event_loop", is_event_loop)

        # req = Req()
        # status_code = await req.test()
        # logger.error(f"{status_code}")

        # t_func.delay()
        # await asyncio.sleep(8)
        # time.sleep(10)
        t_func2.delay()
        await asyncio.sleep(2)
        import sys

        sys.exit(1)
        return HttpResponse("ok")


def tests(request):
    # cc: Country = Country.objects.get(id=1)
    # cc.is_remove = False
    # cc.save()

    t_func2.delay()
    # time.sleep(3)
    import sys

    sys.exit(1)
    return HttpResponse("ok")
