import os
class Config:
    s3_bucket_name = os.environ.get("S3_BUCKET_NAME", "omic-data")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    job_metadata_path = os.environ.get("JOB_METADATA_PATH", "/jobs")


config = Config()
