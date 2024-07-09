FROM public.ecr.aws/sagemaker/sagemaker-distribution:latest-gpu

WORKDIR /opt/ml/code

RUN pip install pandas numpy scikit-learn

COPY src/train.py .

ENTRYPOINT ["python", "train.py"]
