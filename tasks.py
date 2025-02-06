from celery import Celery
import time
import random

# PostgreSQL Backend
celery_pg = Celery("tasks", broker="sqla+postgresql://celery_user:celery_pass@postgres:5433/celery_db",
                    backend="db+postgresql://celery_user:celery_pass@postgres:5433/celery_db")

# Redis Backend
celery_redis = Celery("tasks", broker="redis://redis_broker:6380/0", backend="redis://redis_broker:6380/0")


@celery_pg.task
@celery_redis.task
def simulate_heavy_task(task_name):
    sleep_time = random.uniform(0.5, 3.0)  # Simulates a heavy task
    time.sleep(sleep_time)
    return f"Task {task_name} completed in {sleep_time:.2f} seconds."


def bulk_insert_tasks(celery_client, num_tasks=100):
    start_time = time.time()
    for i in range(num_tasks):
        celery_client.send_task("tasks.simulate_heavy_task", args=[f"Task-{i}"])
    elapsed_time = time.time() - start_time
    return elapsed_time
