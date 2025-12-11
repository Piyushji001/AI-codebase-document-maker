import os
import time
import shutil
import redis
import boto3
import requests
from celery import Celery
from git import Repo
from botocore.exceptions import NoCredentialsError

# Configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
S3_ENDPOINT = os.getenv("S3_ENDPOINT_URL", "http://minio:9000")
# If S3_ENDPOINT is empty, boto3 will use real AWS S3
MINIO_ENDPOINT = S3_ENDPOINT if S3_ENDPOINT else None
MINIO_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID", "minioadmin")
MINIO_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "minioadmin")
BUCKET_NAME = os.getenv("AWS_BUCKET_NAME", "codebase-docs")

# Initialize Celery
app = Celery('tasks', broker=REDIS_URL, backend=REDIS_URL)

# Initialize Redis for status updates
r = redis.from_url(REDIS_URL, decode_responses=True)

def update_status(job_id, status, message):
    r.hset(f"job:{job_id}", mapping={
        "status": status,
        "message": message
    })
    print(f"[Job {job_id}] {status}: {message}")

@app.task(name="tasks.document_repo")
def document_repo(job_id, repo_url):
    try:
        update_status(job_id, "processing", "Starting documentation job")
        
        # 1. Clone Repo
        repo_path = clone_repo_task(job_id, repo_url)
        
        # 2. Parse Codebase (Placeholder)
        file_structure = parse_codebase_task(job_id, repo_path)
        
        # 3. AI Agent (Placeholder)
        docs_content = call_ai_agent_task(job_id, file_structure)
        
        # 4. Generate Site (Placeholder - just zipping for now)
        zip_path = generate_docs_site_task(job_id, docs_content, repo_path)
        
        # 5. Upload to S3
        s3_url = upload_to_s3_task(job_id, zip_path)
        
        # Cleanup
        if os.path.exists(repo_path):
            shutil.rmtree(repo_path)
        if os.path.exists(zip_path):
            os.remove(zip_path)

        # Final Success
        r.hset(f"job:{job_id}", mapping={
            "status": "completed",
            "message": "Documentation generated successfully",
            "download_url": s3_url
        })
        
    except Exception as e:
        update_status(job_id, "failed", str(e))
        raise e

def clone_repo_task(job_id, repo_url):
    update_status(job_id, "cloning", f"Cloning {repo_url}...")
    repo_path = f"/tmp/repos/{job_id}"
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)
    Repo.clone_from(repo_url, repo_path)
    return repo_path

def parse_codebase_task(job_id, repo_path):
    update_status(job_id, "parsing", "Reading file structure...")
    # TODO: Implement actual parsing
    time.sleep(2) # Simulate work
    return {"files": ["main.py", "utils.py"]}

def call_ai_agent_task(job_id, file_structure):
    update_status(job_id, "generating", "AI Agent is analyzing code...")
    
    # Call the Agent Service - use env var for production
    agent_url = os.getenv("AGENT_URL", "http://agent:8001") + "/analyze"
    repo_path = f"/tmp/repos/{job_id}"
    
    try:
        response = requests.post(agent_url, json={"repo_path": repo_path})
        response.raise_for_status()
        return response.json() # Returns dict of {filename: doc_content}
    except Exception as e:
        print(f"Agent failed: {e}")
        # Fallback for demo if agent fails (e.g. no API key)
        return {"README.md": f"# Analysis Failed\n\nError: {str(e)}"}

def generate_docs_site_task(job_id, docs_content, repo_path):
    update_status(job_id, "building", "Building documentation site...")
    
    docs_dir = f"/tmp/docs_site_{job_id}"
    if os.path.exists(docs_dir):
        shutil.rmtree(docs_dir)
    os.makedirs(docs_dir)
    
    # Write generated docs
    if isinstance(docs_content, dict):
        for filename, content in docs_content.items():
            # Handle subdirectories in filenames if present
            safe_name = filename.replace("..", "").replace("/", "_") 
            if not safe_name.endswith(".md"):
                safe_name += ".md"
            
            with open(os.path.join(docs_dir, safe_name), "w", encoding="utf-8") as f:
                f.write(content)
    else:
        # Fallback if content is string
        with open(os.path.join(docs_dir, "README.md"), "w", encoding="utf-8") as f:
            f.write(str(docs_content))

    # Zip the docs directory
    zip_base = f"/tmp/docs_{job_id}"
    shutil.make_archive(zip_base, 'zip', docs_dir)
    return f"{zip_base}.zip"

def upload_to_s3_task(job_id, zip_path):
    update_status(job_id, "uploading", "Finalizing documentation...")
    
    # Check if we have S3 credentials
    if not MINIO_ACCESS_KEY or not MINIO_SECRET_KEY:
        # Fallback to Local Storage (Ephemeral)
        file_name = f"docs_{job_id}.zip"
        storage_dir = "/tmp/storage"
        os.makedirs(storage_dir, exist_ok=True)
        target_path = os.path.join(storage_dir, file_name)
        
        # Move zip to storage dir
        shutil.move(zip_path, target_path)
        
        # Construct download URL
        # In Render, RENDER_EXTERNAL_URL is set automatically
        base_url = os.getenv("RENDER_EXTERNAL_URL", "http://localhost:8000")
        return f"{base_url}/files/{file_name}"

    # S3 Upload Logic
    from botocore.client import Config
    
    # Use localhost endpoint for URL generation so presigned URLs work from browser
    s3_upload = boto3.client('s3',
                      endpoint_url=MINIO_ENDPOINT,
                      aws_access_key_id=MINIO_ACCESS_KEY,
                      aws_secret_access_key=MINIO_SECRET_KEY)
    
    file_name = f"docs_{job_id}.zip"
    
    # Ensure bucket exists
    try:
        s3_upload.create_bucket(Bucket=BUCKET_NAME)
    except Exception:
        pass # Bucket might exist

    s3_upload.upload_file(zip_path, BUCKET_NAME, file_name)
    
    # Create a separate client for presigned URL generation with localhost endpoint
    s3_presign = boto3.client('s3',
                              endpoint_url='http://localhost:9000',
                              aws_access_key_id=MINIO_ACCESS_KEY,
                              aws_secret_access_key=MINIO_SECRET_KEY,
                              config=Config(signature_version='s3v4'))
    
    url = s3_presign.generate_presigned_url('get_object',
                                            Params={'Bucket': BUCKET_NAME,
                                                    'Key': file_name},
                                            ExpiresIn=3600)
        
    return url
