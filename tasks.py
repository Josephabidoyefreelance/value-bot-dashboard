from celery import Celery

# Celery configuration
celery_app = Celery(
    "tasks",
    broker="redis://redis:6379/0",
    backend="db+postgresql://postgres:password@db:5432/postgres"
)

@celery_app.task
def add(x, y):
    return x + y
