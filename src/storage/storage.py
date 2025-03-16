import boto3
from src import config
import logging
from src import JobStatus


class S3StorageAccessor:
    def __init__(self):
        self.s3_client = boto3.client("s3")
        self.bucket = config.s3_bucket_name
        self.logger = logging.getLogger(self.__class__.__name__)

    def upload_model_checkpoint(self, local_path, job_id, file_name):
        s3_object_key = f"checkpoint/{job_id}/{file_name}"
        try:
            self.s3_client.upload_file(local_path, self.bucket, s3_object_key)
            self.logger.log(logging.INFO, f"Successfully uploaded {file_name} to S3 bucket")
            return JobStatus.SUCCESS
        except Exception as e:
            self.logger.log(logging.ERROR, f"Failed to upload {file_name} due to Exception {e}")
            return JobStatus.FAILED

    def get_file_stream(self, object_key, chunk_size=8192):
        try:
            response = self.s3_client.get_object(Bucket=self.bucket, Key=object_key)

            if response and 'Body' in response:
                reader = response['Body']
            else:
                self.logger.log(logging.ERROR, f"Failed to fetch {object_key} stream due to response being empty")
                return JobStatus.FAILED

            chunk = reader.read(chunk_size)
            while chunk:
                yield chunk
                chunk = reader.read(chunk_size)

        except Exception as e:
            self.logger.log(logging.ERROR, f"Failed to fetch {object_key} stream due to Exception {e}")
            return JobStatus.FAILED

    def get_dataset_info(self, data_path):
        if not data_path.startswith("s3://"):
            return {
                "path": data_path,
                "is_s3": False
            }

        prefixes = data_path[:5].split("/", 1)
        if len(prefixes) != 2 or prefixes[0] != self.bucket:
            self.logger.log(logging.ERROR, f"Incorrect path passed")
            return None

        object_key = prefixes[1]
        try:
            response = self.s3_client.head_object(Bucket = self.bucket, Key = object_key)

            if not response:
                self.logger.log(logging.ERROR, f"Failed to fetch metadata for {object_key} due to empty response")
                return JobStatus.FAILED

            return {
                "path": data_path,
                "key": object_key,
                "is_s3": True,
                "size": response.get("ContentLength", 0),
                "last_modified": response.get("LastModified")
            }

        except Exception as e:
            self.logger.log(logging.ERROR, f"Failed to fetch dataset info for {data_path} stream due to Exception {e}")
            return JobStatus.FAILED



