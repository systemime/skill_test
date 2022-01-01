"""
重载django-beat-celery获取django数据库部分, 以尊重django多数据库路由
"""
from functools import partial

from django.db import router, transaction
from django_celery_beat.schedulers import DatabaseScheduler


class SQDatabaseSchedule(DatabaseScheduler):
    def sync(self):
        with transaction.atomic(using=router.db_for_write(self.Model)):
            super().sync()

    def schedule_changed(self):
        db = router.db_for_write(self.Model)
        transaction.commit = partial(transaction.commit, using=db)
        super().schedule_changed()
