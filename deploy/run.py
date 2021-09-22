# https://docs.gunicorn.org/en/stable/settings.html#config
import os  # noqa
from pathlib import Path

"""
# import gevent.monkey
# gevent.monkey.patch_all()
"""
project_path = Path(__file__).resolve().parent.parent

debug = True
loglevel = "info"
bind = "0.0.0.0:60013"  # 监听
# 工作目录
chdir = str(project_path)

# pid文件位置
pidfile = "logs/gunicorn.pid"
# 日志位置
# logfile = 'logs/debug.log'

daemon = False  # 是否是守护进程（后台运行）

# 启动的进程数
# workers = os.cpu_count()
workers = 2
# 指定每个进程开启的线程数
threads = 1

worker_class = "deploy.uvicorn_worker.SQUvicornWorker"  # 重载uvicorn worker
"""
# worker_class = 'gunicorn.workers.ggevent.GeventWorker'  # 协程模式
# worker_class = 'uvicorn.workers.UvicornWorker'  # 原生uvicorn模式
"""

worker_connections = 5000  # 并发客户端的最大数量
max_requests = 4000  # worker在重新启动之前将处理的最大请求数 0 禁止自动重启
max_requests_jitter = 200  # max_requests 抖动

timeout = 60  # 未工作的worker沉默timeout后重启
graceful_timeout = 30  # 重启前给予该时间完成工作

keep_alive = 5  # 等待链接秒数

reload = True

x_forwarded_for_header = "X-FORWARDED-FOR"

# 访问日志文件
# accesslog = str(project_path / "logs/gunicorn_access.log")
# 错误日志文件
# errorlog = str(project_path / "logs/gunicorn_error.log")
# 设置gunicorn访问日志格式，错误日志无法设置
# access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'

"""
gunicorn -c example.py try:app
其每个选项的含义如下：
h          remote address
l          '-'
u          currently '-', may be user name in future releases
t          date of the request
r          status line (e.g. ``GET / HTTP/1.1``)
s          status
b          response length or '-'
f          referer
a          user agent
T          request time in seconds
D          request time in microseconds
L          request time in decimal seconds
p          process ID
"""
