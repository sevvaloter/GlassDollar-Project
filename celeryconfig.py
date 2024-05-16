from celery import Celery

broker_url = "redis://127.0.0.1:6379/0"
result_backend = "redis://127.0.0.1:6379/0"
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
enable_utc = True
timezone = 'UTC'