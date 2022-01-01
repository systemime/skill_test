from urllib.parse import quote  # noqa

from kombu import Exchange, Queue

from .env import env

# FIXME: 使用redis作为celery队列任务长且运行时间长时，retry概率出现无限重试，过期时间失效，最大重试限制失效，worker随机卡死等问题
# FIXME: 推荐rabbitmq
CELERY_BROKER_URL = env(
    "CELERY_BROKER_URL",
    default=env("REDIS_URL").format(f":{env('REDIS_PASSWD', default='')}"),
)
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND", default=CELERY_BROKER_URL)

if env.bool("REDIS_IS_SSL", False):
    BROKER_USE_SSL = env.dict("BROKER_USE_SSL")
    CELERY_REDIS_BACKEND_USE_SSL = env.dict("CELERY_REDIS_BACKEND_USE_SSL")

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
CELERY_BROKER_TRANSPORT_OPTIONS = env.dict(
    "CELERY_BROKER_TRANSPORT_OPTIONS", default={"visibility_timeout": 60 * 60 * 24 * 7}
)

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


# CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERY_BEAT_SCHEDULER = "skill_test.libs.schedulers:SQDatabaseSchedule"
