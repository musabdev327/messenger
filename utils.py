from datetime import datetime


def format_date(timestamp_str):
    return timestamp_str.strftime("%B %d,%Y %H:%M:%S")

def generate_S3_url(bucket_name, aws_region, file_name):
    return f"https://{bucket_name}.s3.{aws_region}.amazonaws.com/{file_name}"
