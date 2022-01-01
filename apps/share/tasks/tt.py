import logging
import time

from asgiref.sync import async_to_sync
from celery import group

from apps.share.req_test.client import req
from skill_test.celery_app import app

logger = logging.getLogger(__name__)


async def func1():
    await req.test()


@app.task(bind=True)
def func(self):
    logger.warning("Test")
    time.sleep(2)
    async_to_sync(func1)()


@app.task(bind=True)
def func2(self):

    tasks = []
    for _ in range(20):
        time.sleep(1)
        tasks.append(func.s())
    group(tasks).apply_async()
