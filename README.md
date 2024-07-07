
---

## Setting Up AWS Infrastructure and Project Environment

### Step 1: Create an AWS Account

If you don't already have an AWS account, go to the [AWS homepage](https://aws.amazon.com/) and click on "Create an AWS Account". Follow the instructions to set up your account.

### Step 2: Log in to the AWS Management Console

1. Navigate to the [AWS Management Console](https://aws.amazon.com/console/).
2. Enter your AWS account credentials (email address and password) to log in.

### Step 3: Set Up IAM Users (Optional but Recommended for Security)

IAM (Identity and Access Management) allows you to manage users and their level of access to AWS services and resources. It's good practice to create an IAM user with limited permissions instead of using your root account for daily tasks.

1. Go to the IAM console by searching for "IAM" in the AWS Management Console or directly [here](https://console.aws.amazon.com/iam/).
2. Click on **Users** in the left sidebar, then click **Add user**.
3. Enter a user name, select **Programmatic access**, and click **Next: Permissions**.
4. Attach policies according to your needs (e.g., `AdministratorAccess` for full access, or custom policies for limited access).
5. Click through to **Review** and then **Create user**. Make sure to download or copy the **Access key ID** and **Secret access key** for future use.

### Step 4: Set Up IAM Roles for Amazon SageMaker

IAM roles are used to grant permissions for SageMaker operations like accessing S3 buckets, running training jobs, and deploying models.

#### Creating an IAM Role for SageMaker

1. In the IAM console, click on **Roles** in the left sidebar, then **Create role**.
2. Choose **AWS service** as the type of trusted entity.
3. Select **SageMaker** from the list of services.
4. Click **Next: Permissions**.
5. Attach policies that grant necessary permissions (e.g., `AmazonSageMakerFullAccess`, `AmazonS3FullAccess`, or custom policies).
6. Click **Next: Tags** to add tags if needed, then **Next: Review**.
7. Give your role a descriptive name (e.g., `SageMakerExecutionRole`) and an optional description.
8. Click **Create role**.

### Step 5: Set Up an S3 Bucket

Amazon S3 (Simple Storage Service) is used to store your dataset, model artifacts, and other project resources.

1. Go to the [Amazon S3 console](https://s3.console.aws.amazon.com/s3/).
2. Click **Create bucket**.
3. Enter a unique bucket name, select a region, and click **Next**.
4. Configure options if needed (such as versioning or encryption), and click **Next**.
5. Review your settings and click **Create bucket**.

### Step 6: Configure AWS CLI (Optional but Recommended)

The AWS Command Line Interface (CLI) allows you to manage AWS services from the command line.

1. Install the AWS CLI by following the instructions for your operating system [here](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html).
2. Configure the AWS CLI with the Access Key ID, Secret Access Key, region, and output format:

   ```sh
   aws configure
   ```

   Follow the prompts to enter your credentials.

### Step 7: Verify Your Setup

After setting up your AWS account, IAM users, roles, and S3 bucket, verify that you can access these resources programmatically (e.g., using AWS CLI or SDKs) and through the AWS Management Console.

### Step 8: Additional Steps (Depending on Your Use Case)

Depending on your specific use case, you may need to:

- Set up VPC (Virtual Private Cloud) for network isolation.
- Configure CloudWatch for monitoring.
- Set up AWS CloudTrail for auditing.
- Configure other AWS services like Amazon RDS (Relational Database Service) or AWS Lambda if needed.

## Setting Up the AIML Ops Project Environment

### Step 1: Create a Folder Structure

Begin by creating a directory for your project and navigating into it:

```sh
mkdir aimlops-project
cd aimlops-project
```

### Step 2: Initialize a Git Repository

Initialize a Git repository for version control:

```sh
git init
```

### Step 3: Set Up Folder Structure and Files

Create the necessary folders and essential files:

```sh
mkdir -p data/{raw,processed} {models,notebooks,src} && touch {models,notebooks,src}/{__init__.py,data_ingestion.py,data_preprocessing.py,train.py,predict.py} .gitignore README.md requirements.txt
mkdir -p data/raw
touch data/raw/sample_data.csv
```

Populate `sample_data.csv` with:

```csv
id,name,age,city
1,John Doe,30,New York
2,Jane Smith,25,San Francisco
3,Mike Johnson,40,Chicago
4,Emily Brown,35,Los Angeles
5,David Lee,28,Miami
```

Your project structure should look like this:

```
aimlops-project/
│
├── data/
│   ├── raw/
│   └── processed/
├── models/
├── notebooks/
├── src/
│   ├── __init__.py
│   ├── data_ingestion.py
│   ├── data_preprocessing.py
│   ├── train.py
│   └── predict.py
├── .gitignore
├── README.md
└── requirements.txt
```

### Step 4: Define Dependencies

Specify the necessary Python libraries in `requirements.txt`:

```txt
boto3
awswrangler
pandas
fastapi
uvicorn
sagemaker
numpy>=1.23.5
```

### Step 5: Implement IAM Roles and Policies for Amazon SageMaker

Follow these steps to set up IAM roles and policies for SageMaker:

1. **Log in to the AWS Management Console**
   - Go to the [IAM console](https://console.aws.amazon.com/iam/).

2. **Create an IAM Role**
   - Navigate to **Roles** > **Create role**.
   - Select **AWS service** as the type of trusted entity.
   - Choose **SageMaker** from the list of services.

3. **Permissions**
   - Click **Next: Permissions**.
   - Attach policies such as `AmazonSageMakerFullAccess` and `AmazonS3FullAccess`.

4. **Tags** (optional)
   - Add tags if needed.
   - Click **Next: Review**.
   - Review the details and click **Create role**.

5. **Attach Policies**
   - Click on the role name after creation.
   - Go to the **Permissions** tab and click **Attach policies**.
   - Select the necessary policies and click **Attach policy**.

6. **Note the Role ARN**
   - Note down the **Role ARN** for later use in configuring SageMaker.

### Step 6: Configure SageMaker to Use the IAM Role

1. Use the IAM role ARN in your SageMaker scripts or resource configurations.

   ```python
   import sagemaker

   role = 'arn:aws:iam::YOUR_ACCOUNT_ID:role/SageMakerExecutionRole'

   # Example of using the role when creating a SageMaker Estimator
   estimator = sagemaker.estimator.Estimator(
       role=role,
       # Other parameters...
   )
   ```

   Replace `YOUR_ACCOUNT_ID` with your AWS account ID and `SageMakerExecutionRole` with your actual role name.

### Step 7: Implement Python Scripts for AIML Ops Pipeline

#### `src/data_ingestion.py`

Handles uploading data to S3:

```python
import boto3

def upload_to_s3(local_file, bucket, s3_file):
    s3_client = boto3.client('s3')
    s3_client.upload_file(local_file, bucket, s3_file)
    print(f"Uploaded {local_file} to s3://{bucket}/{s3_file}")

if __name__ == "__main__":
    upload_to_s3('data/raw/sample_data.csv', 'my-aiml-bucket', 'raw_data/sample_data.csv')
```

#### `src/data_preprocessing.py`

Performs data preprocessing using AWS Wrangler:

```python
import awswrangler as wr

def preprocess_data(input_path, output_path):
    df = wr.s3.read_csv(input_path)
    df_cleaned = df.dropna()  # Example preprocessing step (customize as needed)
    wr.s3.to_csv(df_cleaned, output_path)
    print(f"Preprocessed data saved to {output_path}")

if __name__ == "__main__":
    preprocess_data('s3://my-aiml-bucket/raw_data/sample_data.csv', 's3://my-aiml-bucket/processed_data/cleaned_data.csv')
```

#### `src/train.py`

Script for training the machine learning model using SageMaker:

```python
import sagemaker
from sagemaker import get_execution_role

def train_model(training_data_uri, output_path):
    sagemaker_session = sagemaker.Session()
    role = get_execution_role()

    estimator = sagemaker.estimator.Estimator(
        image_uri='your-training-image',
        role=role,
        instance_count=1,
        instance_type='ml.m5

.large',
        output_path=output_path,
        sagemaker_session=sagemaker_session
    )

    estimator.set_hyperparameters(batch_size=100, epochs=10)  # Example hyperparameters (customize as needed)
    estimator.fit({'train': training_data_uri})
    print(f"Model training completed. Output saved to {output_path}")

if __name__ == "__main__":
    train_model('s3://my-aiml-bucket/processed_data/cleaned_data.csv', 's3://my-aiml-bucket/model_output/')
```

#### `src/predict.py`

Sets up a FastAPI app for model predictions:

```python
from fastapi import FastAPI
import boto3
import json

app = FastAPI()

@app.post("/predict")
async def predict(data: dict):
    sagemaker_runtime = boto3.client('runtime.sagemaker')

    response = sagemaker_runtime.invoke_endpoint(
        EndpointName='your-endpoint-name',
        ContentType='application/json',
        Body=json.dumps(data)
    )

    result = json.loads(response['Body'].read().decode())
    return {"prediction": result}
```

### Step 8: Deploying FastAPI Application for Prediction

1. Install FastAPI and Uvicorn:

   ```sh
   pip install fastapi uvicorn
   ```

2. Start the FastAPI application:

   ```sh
   uvicorn src.predict:app --host 0.0.0.0 --port 8000
   ```

   This starts a web server on `http://localhost:8000` where you can send POST requests to `/predict` with JSON data to get predictions from your SageMaker model.

### Step 9: Monitoring and Maintenance

- **CloudWatch Alarms:** Set up alarms in AWS CloudWatch to monitor SageMaker endpoints for metrics like CPU utilization, error rates, etc.
  
- **Model Monitoring:** Utilize SageMaker Model Monitor to track model performance and data quality over time, ensuring your deployed model remains accurate and reliable.