import os
import boto3
from utils import generate_S3_url
from dotenv import load_dotenv

load_dotenv() 

class S3Client:
    def __init__(self):
        self.session = boto3.session.Session()
        self.aws_region = os.environ.get("AWS_REGION")
        self.bucket_name = os.environ.get("AWS_S3_BUCKET_NAME",)
        self.s3 = self.session.client(
            service_name="s3",
            region_name=self.aws_region,
            aws_access_key_id=os.environ.get("AWS_ACCESS_PUBLIC_KEY"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        )

    def upload_to_s3(self, file_name, file_path):
        if not file_path:
            raise ReferenceError("File path is empty." +
                "Please provide a valid file path.")
            
        full_path = os.path.basename(file_path)
        print(f"Uploading {file_name} to S3")

        try:
            self.s3.upload_file(
                Filename=file_path,
                Bucket=self.bucket_name,
                Key=file_name,
            )
        except Exception as exc:
            print(f"[ERROR] Failed to upload {file_name} to S3")
            return

        return generate_S3_url(self.bucket_name, self.aws_region, file_name)