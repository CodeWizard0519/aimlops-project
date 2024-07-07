Here's a nicely formatted version of your guide:

---

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

### Step 7: Implement Python Scripts

Implement the following scripts under `src/` for your AIML Ops pipeline:

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
    df_cleaned = df.dropna()
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
        instance_type='ml.m5.large',
        output_path=output_path,
        sagemaker_session=sagemaker_session
    )

    estimator.set_hyperparameters(batch_size=100, epochs=10)
    estimator.fit({'train': training_data_uri})
    print(f"Model training completed. Output saved to {output_path}")

if __name__ == "__main__":
    train_model('s3://my-aiml-bucket/processed_data/cleaned_data.csv', 's3://my-aiml-bucket/model_output/')
```

#### `src/predict.py`

FastAPI application for making predictions:

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

### Step 8: Set Up GitHub Actions Workflow

Create a GitHub Actions workflow for CI/CD. Add a `.github/workflows/main.yml` file:

```yaml
name: AIMLOps CI/CD

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run tests
      run: |
        # Add your test scripts here
        echo "Running tests..."
```

### Step 9: Commit and Push to GitHub

Commit your changes and push to your GitHub repository:

```sh
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/aimlops-project.git
git push -u origin master
```

### Step 10: Execute the Pipeline

1. **Data Ingestion**: Run `src/data_ingestion.py` to upload raw data to S3.
2. **Data Preprocessing**: Execute `src/data_preprocessing.py` to clean and preprocess the data.
3. **Model Training**: Run `src/train.py` to train the model and save the output to S3.
4. **Model Deployment**: Deploy the trained model using SageMaker and create an endpoint.
5. **Prediction API**: Start the FastAPI application using Uvicorn:

   ```sh
   uvicorn src.predict:app --host 0.0.0.0 --port 8000
   ```

### Step 11: Monitoring and Maintenance

1. **CloudWatch Alarms**: Set up alarms to monitor SageMaker endpoint metrics.
2. **Model Monitoring**: Utilize SageMaker Model Monitor for tracking model performance and data quality.

### Summary

Follow these steps to establish a robust AIML Ops pipeline using FastAPI and SageMaker, facilitating efficient development, deployment, and maintenance of your machine learning applications. Adjust paths, AWS credentials, and specifics to match your project requirements.

---

This format should help organize your setup process clearly and effectively.