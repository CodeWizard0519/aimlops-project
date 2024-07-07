import awswrangler as wr

def preprocess_data(input_path, output_path):
    df = wr.s3.read_csv(input_path)
    df_cleaned = df.dropna()
    wr.s3.to_csv(df_cleaned, output_path)
    print(f"Preprocessed data saved to {output_path}")

if __name__ == "__main__":
    preprocess_data('s3://my-aiml-bucket/raw_data/sample_data.csv', 's3://my-aiml-bucket/processed_data/cleaned_data.csv')
