# test_embedding_vectors.py
import os
import pandas as pd
from embeddingsVectors import EmbeddingVectors

# Initialize the EmbeddingVectors client
embedding_vectors = EmbeddingVectors(
    api_key=os.environ["OPENAI_API_KEY"],
    api_version="2024-02-01",
    azure_endpoint="https://tu-openai-api-management.azure-api.net/oltatkull/openai/deployments/IDS2024_MATETSKI_EMBEDDING/embeddings?api-version=2024-02-01"
)

# Define the path to the input data file
input_datapath = "TestScripts/embeddingVector/testData/publications_test_data.csv"

# Load the data from the CSV file
df = pd.read_csv(input_datapath, encoding="utf-8", sep=",")

# Combine the relevant columns into a single column
df["combined"] = df["Authors"] + " " + df["Title"] + " " + df["AbstractInEnglish"]

# Insert the embeddings into the database
embedding_vectors.insert_embeddings(df)

# Define the prompt
# prompt = "Research where was applied AI"

# Extract the embedding for the prompt
# prompt_embedding = embedding_vectors.extract(prompt)

# Find the 5 nearest vectors
# nearest_vectors = embedding_vectors.getNearestEmbedding(prompt, n=5)

# Print the metadata of the nearest vectors
# print("Nearest vectors metadata:")
# for metadata in nearest_vectors:
    # print(metadata)
