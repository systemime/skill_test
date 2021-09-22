"""
Django settings for skill_test project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
from urllib.parse import quote  # noqa

import environs
import faker
from kombu import Exchange, Queue

faker = faker.Faker("zh_CN")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# 项目目录
BASE_DIR = Path(__file__).resolve().parent.parent.parent
# 项目主目录
PROJECT_DIR = Path(__file__).resolve().parent.parent
env = environs.Env()
env.read_env(str(BASE_DIR / "env/.local"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# TEMPORARY_KEY = faker.password(
#     length=128, special_chars=True, digits=True, upper_case=True, lower_case=True
# )
ENV_FLAG = env("ENV_FLAG")
SECRET_KEY = env.str("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", True)

ALLOWED_HOSTS = ["*"]

# Application definition
# django内部app
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 自定义及重载django-admin
    "skill_test.libs.commands",
]

# 第三方模块app
MODEL_APPS = [
    "channels",
    "rest_framework",
]

# 项目app
PROJECT_APPS = ["apps.share"]

INSTALLED_APPS = DJANGO_APPS + MODEL_APPS + PROJECT_APPS

MIDDLEWARE = [  # django中间件介绍 https://docs.djangoproject.com/zh-hans/3.1/ref/middleware/
    # 安全性增强
    "django.middleware.security.SecurityMiddleware",
    # 回话session检测或清空
    "django.contrib.sessions.middleware.SessionMiddleware",
    # 通用操作中间件 详见 django/middleware/common.py
    "django.middleware.common.CommonMiddleware",
    # csrftoken 攻击拦截
    "django.middleware.csrf.CsrfViewMiddleware",
    # 请求与用户关联
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    # 处理临时回话
    "django.contrib.messages.middleware.MessageMiddleware",
    # 设置 X-Frame-Options HTTP 响应头
    # 站点可以通过确保网站没有被嵌入到别人的站点里面，从而避免 clickjacking 攻击
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "skill_test.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "skill_test.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
    "default": {},
    "skill_db_system": {
        "ENGINE": "skill_test.libs.db.backends.mysql",
        "NAME": env.str("MYSQL_DATABASE_NAME_system", default="skill_db_system"),
        "USER": env.str("MYSQL_USER_system", "root"),
        "PASSWORD": env.str("MYSQL_PASSWORD_system", default="127.0.0.1"),
        "HOST": env.str("MYSQL_HOST_system", default="127.0.0.1"),
        "PORT": env.str("MYSQL_PORT_system", default="33060"),
        "TEST": {
            "NAME": env.str("MYSQL_TEST_NAME_system", default="test_db_system"),
            "CHARSET": "utf8",
            "COLLATION": "utf8_general_ci",
        },
        "POOL": {
            # 连接池大小
            "pool_size": 20,
            # 连接池可溢出最大值
            "max_overflow": 10,
            # 等待超时时间
            "timeout": 20,
            # 是否后进先出
            "use_lifo": True,
            # 连接回收时间
            "recycle": 8 * 3600,
            # 日志名称
            "logging_name": "conn_pool",
            # 是否每次校验连接有效
            "pre_ping": True,
        },
    },
    "skill_db_app": {
        "ENGINE": "skill_test.libs.db.backends.mysql",
        "NAME": env.str("MYSQL_DATABASE_NAME_app", default="skill_db_app"),
        "USER": env.str("MYSQL_USER_app", "root"),
        "PASSWORD": env.str("MYSQL_PASSWORD_app", default="127.0.0.1"),
        "HOST": env.str("MYSQL_HOST_app", default="127.0.0.1"),
        "PORT": env.str("MYSQL_PORT_app", default="33060"),
        "TEST": {
            "NAME": env.str("MYSQL_TEST_NAME_app", default="test_db_app"),
            "CHARSET": "utf8",
            "COLLATION": "utf8_general_ci",
        },
        "POOL": {
            "pool_size": 20,
            "max_overflow": 10,
            "timeout": 20,
            "use_lifo": False,
            "recycle": 8 * 3600,
            "logging_name": "conn_pool",
            "pre_ping": True,
        },
    },
}

DATABASE_APPS_MAPPING = {
    "share": "skill_db_app",
}

# APP路由映射
# DATABASE_ROUTERS = ['skill_test.libs.db.db_router.MasterSlaveDBRouter']

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# -- 异步安全选项
# Django的某些关键部分在异步环境中无法安全运行，因为它们的全局状态不支持协同程序。
# Django的这些部分被分类为“异步不安全”，并且受到保护，无法在异步环境中执行。ORM是主要示例，但是其他部分也以这种方式受到保护。
# ---
# 如果您尝试从存在运行中事件循环的线程中运行这些部件中的任何一个，则会收到 SynchronousOnlyOperation错误消息。
# 请注意，您不必直接在异步函数内部即可发生此错误。
# 如果您直接从异步函数中调用了同步函数，而没有使用sync_to_async()或类似方法，则它也可能发生。
# 这是因为您的代码即使未声明为异步代码，也仍在具有活动事件循环的线程中运行。
# ---
# 如果遇到此错误，则应修复代码以免从异步上下文中调用有问题的代码。
# 而是编写自己的与异步不安全函数对话的代码，同步函数，然后使用asgiref.sync.sync_to_async()（或在其自己的线程中运行同步代码的任何其他方式）进行调用 。
# ---
# 您可能仍然被迫从异步上下文中运行同步代码。
# 例如，如果外部环境（例如Jupyter笔记本电脑）强加了您的要求 。
# 如果您确定不可能同时运行代码，并且绝对需要从异步上下文中运行此同步代码，则可以通过设置警告来禁用警告 DJANGO_ALLOW_ASYNC_UNSAFE 环境变量为任何值。
# ---
# https://docs.djangoproject.com/en/3.1/topics/async/#async-safety
# os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
DJANGO_ALLOW_ASYNC_UNSAFE = True

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "zh-Hans"

TIME_ZONE = "Asia/Shanghai"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"  # media资源路径

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ===============================Redis=====================================
REDIS_URL = env("REDIS_URL")
REDIS_PASSWD = env("REDIS_PASSWD")

# ===============================Celery====================================
if USE_TZ:
    CELERY_TIMEZONE = TIME_ZONE

# FIXME: 使用redis作为celery队列任务长且运行时间长时，retry概率出现无限重试，过期时间失效，最大重试限制失效，worker随机卡死等问题
# FIXME: 推荐rabbitmq
CELERY_BROKER_URL = env("CELERY_BROKER_URL", default=REDIS_URL)
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND", default=CELERY_BROKER_URL)

# 结果相关
CELERY_TASK_IGNORE_RESULT = env("CELERY_TASK_IGNORE_RESULT", default=False)
CELERY_TASK_STORE_ERRORS_EVEN_IF_IGNORED = env(
    "CELERY_TASK_STORE_ERRORS_EVEN_IF_IGNORED", default=True
)
CELERY_RESULT_EXPIRES = env("CELERY_RESULT_EXPIRES", default=60 * 60 * 24)

CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
# 任务超时时间
CELERY_TASK_TIME_LIMIT = env("CELERY_TASK_TIME_LIMIT", default=5 * 60)
CELERY_TASK_SOFT_TIME_LIMIT = env("CELERY_TASK_SOFT_TIME_LIMIT", default=60)
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

# 默认的队列 celery
CELERY_DEFAULT_QUEUE = env("CELERY_DEFAULT_QUEUE", default="celery")
CELERY_DEFAULT_ROUTING_KEY = env("CELERY_DEFAULT_ROUTING_KEY", default="celery")
# 默认队列
CELERY_TASK_QUEUES = {
    Queue(CELERY_DEFAULT_QUEUE, routing_key=CELERY_DEFAULT_ROUTING_KEY),
}

# 每个worker执行n个task后重启
CELERYD_MAX_TASKS_PER_CHILD = env.int("CELERYD_MAX_TASKS_PER_CHILD", default=200)
# celery worker 每次去 rabbitMQ 取任务的数量, 日后需要区分低频与高频任务分开设置
CELERYD_PREFETCH_MULTIPLIER = env.int("CELERYD_PREFETCH_MULTIPLIER", default=40)

# 读取环境变量动态增加 Celery routes 和 queues
env_celery_routes = env.json("CELERY_ROUTES", default=None)
if env_celery_routes is not None:
    CELERY_TASK_ROUTES = {}
    for item in env_celery_routes:
        # 添加一个 queue [rabbitmq]
        CELERY_TASK_QUEUES.add(
            Queue(
                item["name"],
                exchange=Exchange(item["name"]),
                routing_key=item["routing_key"],
            )
        )
        # 添加一个 queue [redis]
        # CELERY_TASK_QUEUES.add(
        #     Queue(
        #         item["name"],
        #         exchange=item["name"],
        #         routing_key=item["routing_key"]
        #     )
        # )
        # 添加一个 route
        CELERY_TASK_ROUTES.update(
            {
                item["path"]: {
                    "queue": item["name"],
                    "routing_key": item["routing_key"],
                }
            }
        )

# ==============================Cache======================================

# MemcachedCache 缓存替换原则是LRU算法（速度快，安全性低，数据格式简单，弃用换redis）
CACHES = {
    "default": {
        # 指定缓存使用的引擎
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",  # 激活数据压缩
            "KEY_PREFIX": "skill_test",
            # 特定缓存键值对，每个项目均不同，防止不同项目之间的缓存实例混用，不设置本项(不要为空)django自动设置
            "IGNORE_EXCEPTIONS": True,
            # 防止redis意外关闭造成异常，memcached backend 的默认行为 django-redis配置项
            "PASSWORD": REDIS_PASSWD,
        },
    }
}

# ==============================Channel====================================
ASGI_APPLICATION = "skill_test.asgi.application"

# quote(REDIS_PASSWD)

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            # "hosts": [('127.0.0.1', 6379)],
            "hosts": [f"redis://:{REDIS_PASSWD}@127.0.0.1:6379/2"],
            "symmetric_encryption_keys": [SECRET_KEY],
        },
    },
}

# =============================Django-hashid===================================
HASHID_FIELD_SALT = env("HASHID_FIELD_SALT")
HASHID_ALPHABETS = env("HASHID_ALPHABETS")
HASHID_FIELD_MIN_LENGTH = env.int("HASHID_FIELD_MIN_LENGTH")
HASHID_FIELD_ALLOW_INT_LOOKUP = env.bool("HASHID_FIELD_ALLOW_INT_LOOKUP", default=True)