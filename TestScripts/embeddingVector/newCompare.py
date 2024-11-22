import os

import pandas as pd
import numpy as np
from ast import literal_eval
from embeddingsVectors import EmbeddingVectors

client = EmbeddingVectors(
    api_key=os.environ["OPENAI_API_KEY"],
    api_version="2024-02-01",
    azure_endpoint="https://tu-openai-api-management.azure-api.net/oltatkull/openai/deployments/IDS2024_MATETSKI_EMBEDDING/embeddings?api-version=2024-02-01"

)

MAX_TOKENS = 8000

datafile_path = "testData/publications_extraction_test_data.csv"

df = pd.read_csv(datafile_path)
df["embedding"] = df.embedding.apply(literal_eval).apply(np.array)

# search through the reviews for a specific product
results = client.getNearestEmbedding(df, """
The aim of this article is to introduce to an audience bourgeois home
interiors in Tallinn of the first quarter of the 19th century through
""", n=3)

print(results.head())