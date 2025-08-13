import os

bind = f"0.0.0.0:{os.environ.get('PORT', '8000')}"

workers = int(os.environ.get('GUNICORN_WORKERS', '3'))

worker_class = 'sync'

timeout = 120

loglevel = 'info'