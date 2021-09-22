"""覆盖django startapp 命令"""
from django.conf import settings
from django.core.management import CommandError
from django.core.management.templates import TemplateCommand


class Command(TemplateCommand):
    def handle(self, **options):
        app_name = options.pop("name")

        if options.pop("directory"):
            raise CommandError("custom directory is not allowed")
        if options.pop("template"):
            raise CommandError("custom template is not allowed")

        target = settings.BASE_DIR / f"apps/{app_name}"

        if not target.exists():
            # 参数说明: 如果中间路径不存在，则创建它
            # 同时忽略存在部分路径错误，不引发FileExistsError错误
            target.mkdir(parents=True, exist_ok=True)

        target = str(target)
        template = settings.PROJECT_DIR / "libs/app_template"  # 使用的app生成模版
        options["template"] = str(template)
        super().handle("app", app_name, target, **options)
