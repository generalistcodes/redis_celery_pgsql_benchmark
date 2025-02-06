import time
import pandas as pd
import matplotlib.pyplot as plt
from tasks import bulk_insert_tasks
from celery import Celery
import requests

# Configure Celery clients for PostgreSQL and Redis
celery_pg = Celery("tasks", broker="sqla+postgresql://celery_user:celery_pass@postgres:5433/celery_db",
                    backend="db+postgresql://celery_user:celery_pass@postgres:5433/celery_db")

celery_redis = Celery("tasks", broker="redis://redis_broker:6380/0", backend="redis://redis_broker:6380/0")

# Function to monitor Celery queue size in Flower
def get_celery_queue_size():
    flower_api = "http://localhost:5556/api/queues"
    try:
        response = requests.get(flower_api)
        if response.status_code == 200:
            queue_data = response.json()
            return queue_data
        else:
            print("[WARNING] Unable to fetch Flower queue data.")
            return None
    except Exception as e:
        print(f"[ERROR] Flower API not reachable: {e}")
        return None


def benchmark_task_submission(celery_client, task_count):
    start_time = time.time()
    for _ in range(task_count):
        celery_client.send_task("tasks.simulate_heavy_task", args=["Benchmark Task"])
    elapsed_time = time.time() - start_time
    return elapsed_time


# Define test cases with different task counts
task_sizes = [10, 100, 500, 1000]
pg_times = []
redis_times = []

for task_count in task_sizes:
    print(f"Running benchmark for {task_count} tasks on PostgreSQL backend...")
    pg_time = benchmark_task_submission(celery_pg, task_count)
    pg_times.append(pg_time)
    
    print(f"Running benchmark for {task_count} tasks on Redis backend...")
    redis_time = benchmark_task_submission(celery_redis, task_count)
    redis_times.append(redis_time)
    
    queue_status = get_celery_queue_size()
    print(f"[INFO] Celery Queue Status: {queue_status}")

# Store results in a DataFrame
results_df = pd.DataFrame({
    "Task Count": task_sizes,
    "PostgreSQL Backend (s)": pg_times,
    "Redis Backend (s)": redis_times
})

# Visualizing results
plt.figure(figsize=(10, 5))
plt.plot(results_df["Task Count"], results_df["PostgreSQL Backend (s)"], marker='o', label="PostgreSQL")
plt.plot(results_df["Task Count"], results_df["Redis Backend (s)"], marker='s', label="Redis")
plt.xlabel("Number of Tasks")
plt.ylabel("Time Taken (seconds)")
plt.title("Task Submission Speed: PostgreSQL vs Redis Backend")
plt.legend()
plt.grid()
plt.show()

# Display DataFrame
display(results_df)
