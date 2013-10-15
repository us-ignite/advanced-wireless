import os
import signal
import sys

bind = '0.0.0.0:8000'
pidfile = '/tmp/gunicorn.pid'
errorlog = 'gunicorn.log'
debug = True
loglevel = 'debug'
workers = 1
worker_class = "gevent"


def post_fork(server, worker):
    from psycogreen.gevent import patch_psycopg
    patch_psycopg()
    worker.log.info("Made psycopg Green")

# Gunicorn autoreload as suggested on https://github.com/benoitc/gunicorn/issues/154
# and https://github.com/benoitc/gunicorn/blob/master/examples/example_gevent_reloader.py


def on_starting(server):
    # use server hook to patch socket to allow worker reloading
    from gevent import monkey
    monkey.patch_socket()


def when_ready(server):
    def monitor():
        modify_times = {}
        while True:
            for module in sys.modules.values():
                path = getattr(module, "__file__", None)
                if not path: continue
                if path.endswith(".pyc") or path.endswith(".pyo"):
                    path = path[:-1]
                try:
                    modified = os.stat(path).st_mtime
                except:
                    continue
                if path not in modify_times:
                    modify_times[path] = modified
                    continue
                if modify_times[path] != modified:
                    server.log.info("%s modified; restarting server", path)
                    os.kill(os.getpid(), signal.SIGHUP)
                    modify_times = {}
                    break
            gevent.sleep(1)

    import gevent
    gevent.spawn(monitor)
