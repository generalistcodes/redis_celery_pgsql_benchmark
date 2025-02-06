import time
from celery import Celery

# PostgreSQL Connection Details
PG_HOST = "localhost"
PG_PORT = 5433
PG_USER = "celery_user"
PG_PASSWORD = "celery_pass"
PG_DATABASE = "celery_db"

# Celery client using PostgreSQL as the backend
celery_pg = Celery(
    "tasks",
    broker=f"sqla+postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}",
    backend=f"db+postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}"
)

def create_task():
    """
    Submits a single task to Celery and prints the task ID.
    """
    try:
        start_time = time.time()
        task = celery_pg.send_task("tasks.simulate_heavy_task", args=["Single Task"])
        elapsed_time = time.time() - start_time
        print(f"✅ Created Task: {task.id} in {elapsed_time:.6f} seconds")
    except Exception as e:
        print(f"[❌] Task creation failed: {e}")

# Run the task creation function
create_task()
