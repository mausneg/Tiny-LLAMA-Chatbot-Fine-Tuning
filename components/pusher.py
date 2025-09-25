import boto3
from botocore.exceptions import ClientError
import os

s3 = boto3.client('s3')
BUCKET_NAME = 'mausneg-mlops'

def create_bucket(bucket_name: str = None):
    region = s3.meta.region_name
    try:
        s3.head_bucket(Bucket=bucket_name)
        print(f"[S3] Bucket {bucket_name} already exists")
    except ClientError as e:
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
            print(f"[S3] Bucket {bucket_name} is created")
        else:
            print(f"[S3] Error checking bucket: {e}")
            raise

def upload_folder(folder_path, s3_prefix):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            local_file = os.path.join(root, file)
            relpath = os.path.relpath(local_file, folder_path)
            s3_key = os.path.join(s3_prefix, relpath)
            s3.upload_file(local_file, BUCKET_NAME, s3_key)
    print(f"[S3] Folder {folder_path} uploaded to bucket {BUCKET_NAME} with prefix {s3_prefix}")

if __name__ == "__main__":
    create_bucket(BUCKET_NAME)
    upload_folder('saved_models/TinyLlama-1.1B-Chat-v1.2', 'saved_models/TinyLlama-1.1B-Chat-v1.2')