import os
import pandas as pd
import json
from openai import AzureOpenAI

client2 = AzureOpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
    api_version="2024-02-01",
    azure_endpoint="https://tu-openai-api-management.azure-api.net/oltatkull/openai/deployments/IDS2024_MATETSKI_EMBEDDING/embeddings?api-version=2024-02-01"
)


def extract(text):
    # Create an embedding
    embedding_response = client2.embeddings.create(
        model="IDS2024_MATETSKI_EMBEDDING",
        input=text
    )

    # Extract the embedding vector
    return embedding_response.data[0].embedding


with open("input.txt", "r") as infile, open("output.txt", "w") as outfile:
    for line in infile:
        embedding_vector = extract(line.strip())
        outfile.write(json.dumps(embedding_vector) + "\n")

