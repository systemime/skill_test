from uvicorn.workers import UvicornWorker


# https://github.com/encode/uvicorn/issues/709
# 重载Uvicorn的work，解决超时问题
class SQUvicornWorker(UvicornWorker):
    CONFIG_KWARGS = {"loop": "uvloop", "http": "httptools", "lifespan": "off"}
