"""
Gunicorn configuration file for statsfut.com
Python format - more reliable than .conf format
"""

import os
import multiprocessing

# Server socket
bind = "0.0.0.0:8095"

# Worker processes
workers = 1
worker_class = "geventwebsocket.gunicorn.workers.GeventWebSocketWorker"
threads = 2
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 30
keepalive = 2

# Process naming
proc_name = 'statsfut'

# Server mechanics
daemon = True
pidfile = '/www/wwwroot/statsfut.com/logs/statsfut.pid'
user = 'www'
group = 'www'
umask = 0o007
tmp_upload_dir = None

# Logging
errorlog = '/www/wwwroot/statsfut.com/logs/error.log'
loglevel = 'info'
accesslog = '/www/wwwroot/statsfut.com/logs/access.log'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = 'statsfut'

# Django WSGI application path
wsgi_app = "core.wsgi:application"

# Environment variables
raw_env = [
    "DJANGO_SETTINGS_MODULE=core.settings",
]

# Preload app for better performance
preload_app = False

# Chdir to specified directory before apps loading
chdir = '/www/wwwroot/statsfut.com'
