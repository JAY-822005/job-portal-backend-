"""
Gunicorn configuration for production
"""

import multiprocessing
import os

# Server binding
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes
workers = max(multiprocessing.cpu_count() - 1, 2)
worker_class = "sync"
worker_connections = 1000
worker_timeout = 60
keepalive = 5

# Request handling
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = "/var/log/job_portal/access.log"
errorlog = "/var/log/job_portal/error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "job_portal_gunicorn"

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL settings (optional, configure as needed)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"
# ssl_version = "TLSv1_2"

# Server hooks
def when_ready(server):
    print("Gunicorn server is ready. Spawning workers")

def on_exit(server):
    print("Gunicorn server is shutting down")
