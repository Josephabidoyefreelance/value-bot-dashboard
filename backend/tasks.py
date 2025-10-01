from celery import Celery
import time

celery_app = Celery(
    "tasks",
    broker="redis://redis:6379/0",
    backend="db+postgresql://postgres:postgres@db:5432/postgres"
)

@celery_app.task
def add_dummy_bet(x, y):
    time.sleep(1)
    return x + y
