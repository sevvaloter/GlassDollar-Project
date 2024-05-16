from fastapi import FastAPI, BackgroundTasks
from tasks import fetch_enterprise_data
import redis
# Initialize FastAPI app
app = FastAPI()

@app.get("/start-crawl/")
def start_crawl(background_tasks: BackgroundTasks):
    result = fetch_enterprise_data.delay()
    task_id = result.id
    background_tasks.add_task(check_task_status, result)
    return {"message": "Task started", "task_id": task_id}

def check_task_status(result):
    import time
    while not result.ready():
        time.sleep(1)
    if result.successful():
        print(result.result)
    else:
        print("Task failed")

@app.get("/task-status/{task_id}")
def get_task_status(task_id: str):
    result = fetch_enterprise_data.AsyncResult(task_id)
    if result.state == 'PENDING':
        response = {"status": "Pending..."}
    elif result.state == 'SUCCESS':
        response = {"status": "Completed", "result": result.get()}
    elif result.state == 'FAILURE':
        response = {"status": "Failed", "result": str(result.info)}
    else:
        response = {"status": "Unknown"}
    return response