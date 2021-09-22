"""增强django migrate 命令
自动迁移所有数据库，由routers控制迁移保证迁移到指定数据库
"""
from django.conf import settings
from django.core.management.commands.migrate import Command as MigrateCommand


class Command(MigrateCommand):
    """
    python manage.py migrate 顺序迁移所有app的数据库模型
    默认迁移顺序为settings的DATABASES配置顺序（除default外）

    兼容--database，使用指定迁移多个数据库，使用英文","分割，迁移顺序为书写顺序
    --database=admin_db,agent_db,test_db

    当migrate后附加除 --database 以外参数时，建议使用单数据库操作
    否则，如fake、run-syncdb等参数可能被应用到所有数据库

    django/db/utils.py已处理可能出现的错误，无需此处定义
    """

    help = (
        "Updates database schema. "
        "Manages both apps with migrations and those without."
    )

    def handle(self, *args, **options):
        database = options.pop("database")
        if database and database != "default":
            db_lists = database.split(",")
        else:
            db_lists = [db for db in settings.DATABASES if db != "default"]
        for db in db_lists:
            options["database"] = db
            super().handle(self, *args, **options)

        # super().handle(self, *args, **options)
