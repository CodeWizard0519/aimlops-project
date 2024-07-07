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
