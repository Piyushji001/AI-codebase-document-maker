from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import redis
import os
import uuid
import json
from dotenv import load_dotenv

load_dotenv()

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Autonomous Codebase Documenter API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For dev, allow all. In prod, specify domain.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redis Connection
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
r = redis.from_url(redis_url, decode_responses=True)

class RepoRequest(BaseModel):
    repo_url: str

@app.get("/")
def read_root():
    return {"message": "Autonomous Codebase Documenter API is running"}

@app.post("/start-documentation")
def start_documentation(request: RepoRequest):
    # Validate URL (basic check)
    if not request.repo_url.startswith("http"):
        raise HTTPException(status_code=400, detail="Invalid URL")

    job_id = str(uuid.uuid4())
    
    # Initialize job status in Redis
    r.hset(f"job:{job_id}", mapping={
        "status": "queued",
        "repo_url": request.repo_url,
        "message": "Job queued"
    })

    # Push to Celery
    celery_app = redis.from_url(redis_url) # Just using redis client to check, but we need celery to send
    # We use send_task to avoid importing the task code directly
    from celery import Celery
    celery = Celery(broker=redis_url)
    celery.send_task("tasks.document_repo", args=[job_id, request.repo_url])
    
    print(f"Job {job_id} queued for {request.repo_url}")

    return {"job_id": job_id, "status": "queued"}

@app.get("/job-status/{job_id}")
def get_job_status(job_id: str):
    job = r.hgetall(f"job:{job_id}")
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@app.get("/get-docs/{job_id}")
def get_docs(job_id: str):
    job = r.hgetall(f"job:{job_id}")
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job.get("status") != "completed":
        raise HTTPException(status_code=400, detail="Job not completed yet")
        
    return {"download_url": job.get("download_url")}
