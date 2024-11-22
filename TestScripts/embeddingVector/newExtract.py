from codecs import encode
import pandas as pd
import os
from embeddingsVectors import EmbeddingVectors

client = EmbeddingVectors(
    api_key=os.environ["OPENAI_API_KEY"],
    api_version="2024-02-01",
    azure_endpoint="https://tu-openai-api-management.azure-api.net/oltatkull/openai/deployments/IDS2024_MATETSKI_EMBEDDING/embeddings?api-version=2024-02-01"

)

MAX_TOKENS = 8000

input_datapath = "TestScripts/embeddingVector/testData/publications_test_data.csv"

df = pd.read_csv(input_datapath, encoding="utf-8", sep=",")

df = df[["Year", "Authors", "Title", "ImportedKeywords", "AuthorKeywords", "AbstractInEnglish"]]

# Remove rows with any missing values
# df = df.dropna()

df["combined"] = (
        df["Authors"] + " " + df["Title"] + " " + df["AbstractInEnglish"]
)

df["n_tokens"] = df.combined.apply(lambda x: len(encode(str(x), "utf-8")))
df = df[df.n_tokens <= MAX_TOKENS]

df["embedding"] = df.combined.apply(lambda x: client.extract(x))
df.to_csv("publications_extraction_test_data.csv")
