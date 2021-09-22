from django.conf import settings

BUILDIN_LABEL = ("contenttypes",)
DEFAULT_DB = "skill_db_system"


class MasterSlaveDBRouter:
    @staticmethod
    def get_db(model):
        return settings.DATABASE_APPS_MAPPING.get(model._meta.app_label) or DEFAULT_DB

    @staticmethod
    def allow_migrate(db, app_label, model_name=None, **hints):
        """允许迁移"""
        if app_label in BUILDIN_LABEL:
            return True
        return db.startswith(app_label)

    def db_for_read(self, model, **hints):
        """判断读取数据库"""
        return self.get_db(model)

    def db_for_write(self, model, **hints):
        """判断写入数据库"""
        return self.get_db(model)

    def allow_relation(self, obj1, obj2, **hints):
        """是否允许关联"""
        return True


"""手动选择数据库
obj = models.Student.objects.using('deafult').get(pk=3)
"""
