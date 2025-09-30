import boto3
import os

bucket_name = "mausneg-mlops"
s3_prefix = "saved_models"
s3 = boto3.client(
    's3',
    # comment the below two lines in production
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
)

def download_dir(local_path, model_name):
    print(f'[S3] Downloading model {model_name} to {local_path}')
    os.makedirs(local_path, exist_ok=True)
    paginator = s3.get_paginator('list_objects_v2')
    for result in paginator.paginate(Bucket=bucket_name, Prefix=f"{s3_prefix}/{model_name}"):
        if 'Contents' in result:
            for key in result['Contents']:
                s3_key = key['Key']
                local_file = os.path.join(local_path, os.path.relpath(s3_key, s3_prefix))
                os.makedirs(os.path.dirname(local_file), exist_ok=True)
                s3.download_file(bucket_name, s3_key, local_file)
    print(f'[S3] Download completed for model {model_name} to {local_path}')