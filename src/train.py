import boto3
import sagemaker

# Replace with your actual IAM role ARN
AWS_ROLE_ARN = 'arn:aws:iam::767397784105:role/SageMakerRole'


def train_model(training_data_uri, output_path):
    sagemaker_session = sagemaker.Session()

    # Explicitly set the role ARN
    role = AWS_ROLE_ARN

    estimator = sagemaker.estimator.Estimator(
        image_uri='your-training-image',
        role=role,
        instance_count=1,
        instance_type='ml.m5.large',
        output_path=output_path,
        sagemaker_session=sagemaker_session
    )

    estimator.set_hyperparameters(batch_size=100, epochs=10)
    estimator.fit({'train': training_data_uri})
    print(f"Model training completed. Output saved to {output_path}")


if __name__ == "__main__":
    train_model('s3://my-aiml-bucket/processed_data/cleaned_data.csv', 's3://my-aiml-bucket/model_output/')
