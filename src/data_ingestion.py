import boto3

def upload_to_s3(local_file, bucket, s3_file):
    s3_client = boto3.client('s3')
    s3_client.upload_file(local_file, bucket, s3_file)
    print(f"Uploaded {local_file} to s3://{bucket}/{s3_file}")

if __name__ == "__main__":
    upload_to_s3('data/raw/sample_data.csv', 'my-aiml-bucket', 'raw_data/sample_data.csv')
