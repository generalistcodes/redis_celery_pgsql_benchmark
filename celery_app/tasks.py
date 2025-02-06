from celery import Celery

celery_app = Celery("tasks", broker="redis://redis_broker:6379/0")

@celery_app.task
def simulate_heavy_task(data):
    return f"Processed: {data}"
