# Gunicorn configuration file.
bind = '0.0.0.0:8000'
workers = 4
worker_class = 'sync'
worker_connections = 10
timeout = 120
keepalive = 2
loglevel = 'DEBUG'
