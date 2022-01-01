import os

from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "skill_test.settings.base")

app = Celery("skill_test")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# celery后端连接客户端，如果在Task类中使用，可以 `self.backend.client`
client = app.connection().channel().client
# celery worker控制器api，但是获取结果时很慢，最好用异步的形式或者离线的方式去调用
inspect = app.control.inspect()

# flake8: noqa: B950
app.conf.beat_schedule = {
    # 获取 免费代理池 / 5min获取一次
    "get_proxy_pool": {
        "task": "apps.proxy_pool.tasks.proxy_check.get_proxy_pool",
        "schedule": crontab(minute="*/5"),
    },
}
