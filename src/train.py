import os
import boto3
import sagemaker

def train_model(training_data_uri, output_path):
    os.environ['AWS_REGION'] = 'us-east-1'  # Ensure this matches your AWS region
    sagemaker_session = sagemaker.Session()

    role = 'arn:aws:iam::767397784105:role/SageMakerRole'  # Replace with your SageMaker role ARN
    estimator = sagemaker.estimator.Estimator(
        image_uri='767397784105.dkr.ecr.us-east-1.amazonaws.com/mlops:latest',
        role=role,
        instance_count=1,
        instance_type='t3.large',
        output_path=output_path,
        sagemaker_session=sagemaker_session
    )

    estimator.set_hyperparameters(batch_size=100, epochs=10)
    estimator.fit({'train': training_data_uri})
    print(f"Model training completed. Output saved to {output_path}")

if __name__ == "__main__":
    train_model('s3://my-aiml-bucket/processed_data/cleaned_data.csv', 's3://my-aiml-bucket/model_output/')
