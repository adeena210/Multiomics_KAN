import os
import uuid
from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel
from enum import Enum
import datetime
import json

router = APIRouter()

job_directory_path = "jobs"
os.makedirs(job_directory_path, exist_ok=True)


class TrainingJob(BaseModel):
    data_path: str
    meta_path: str
    model_params: dict


class JobStatus(Enum):
    PENDING = 'Pending'
    IN_PROGRESS = 'In Progress'
    PREPROCESSING = 'Preprocessing'
    FAILED = 'Failed'
    SUCCESS = 'Success'


@router.post("/jobs/")
async def create_job(request: TrainingJob, background_tasks: BackgroundTasks):
    job_id = uuid.uuid4()
    job_meta = {
        "id": job_id,
        "status": JobStatus.PENDING,
        "data_path": request.data_path,
        "meta_path": request.meta_path,
        "model_params": request.model_params,
        "progress": 0.0,
        "creation_date_time": str(datetime.datetime.now())
    }

    with open(f"{job_directory_path}/{job_id}.json", "w") as file:
        json.dump(job_meta, file)

    background_tasks.add_task(process_job, job_id)


@router.get("/jobs/{job_id}")
async def get_job(job_id: str):
    job_path = f"{job_directory_path}/{job_id}.json"
    if not os.path.exists(job_path):
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")

    with open(job_path, "r") as file:
        return file
