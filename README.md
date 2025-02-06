# Celery Benchmark: PostgreSQL vs Redis Backend

## Overview
This project benchmarks **Celery task execution time** using two different backends:
- **PostgreSQL** (Database-backed Celery tasks)
- **Redis** (In-memory task storage for faster execution)

The project also includes **real-time queue monitoring** via **Celery Flower**, and a **Jupyter Notebook** for visualization.

---
## Features
✅ **Compare PostgreSQL vs Redis** for task submission time
✅ **Monitor Celery queue size in real-time** using Flower API
✅ **Visualize benchmark results** using Matplotlib
✅ **Supports different task loads** (10, 100, 500, 1000 tasks)

---
## Step-by-Step Setup
### 1. Clone the Repository
```sh
git clone <your-repo-url>
cd celery-benchmark
```

### 2. Start the Docker Environment
```sh
docker-compose up -d
```
This starts:
- **PostgreSQL** (`localhost:5432`)
- **Redis** (`localhost:6379`)
- **Celery Workers** (one for PostgreSQL, one for Redis)
- **Celery Flower UI** (`http://localhost:5555`)
- **PGAdmin** (`http://localhost:8080`)
- **Jupyter Notebook** (`http://localhost:8888`)

### 3. Install Dependencies
```sh
docker exec -it celery_worker_pg pip install -r /app/requirements.txt
docker exec -it celery_worker_redis pip install -r /app/requirements.txt
```

### 4. Access Monitoring Tools
- **Celery Flower**: [http://localhost:5555](http://localhost:5555)
- **PGAdmin**: [http://localhost:8080](http://localhost:8080)
- **Jupyter Notebook**: [http://localhost:8888](http://localhost:8888)

---
## Running the Benchmark
### 1. Open Jupyter Notebook
Navigate to **Jupyter Notebook** (`http://localhost:8888`), open `celery_benchmark_notebook.ipynb`, and **run all cells**.

### 2. Results and Visualization
- The notebook submits tasks to both **PostgreSQL and Redis** backends.
- Measures task submission speed.
- **Plots a comparison graph** of PostgreSQL vs Redis performance.

---
## Monitoring Celery Queue Load
To check if Celery queues are overloaded:
```sh
docker logs celery_worker_pg --follow
docker logs celery_worker_redis --follow
```

Alternatively, visit **Celery Flower UI** (`http://localhost:5555`) to see real-time queue status.

---
## Conclusion
- **PostgreSQL backend is reliable but may slow down under heavy load.**
- **Redis backend is significantly faster for task submission.**
- If task execution speed is critical, **switch to Redis as the backend.**

---
## Next Steps
- **Increase task sizes** (e.g., 5000+ tasks) and compare results.
- **Scale Celery workers dynamically** to handle large queues.
- **Optimize PostgreSQL performance** with connection pooling.

🚀 **Run the benchmark and decide the best backend for your workload!**

