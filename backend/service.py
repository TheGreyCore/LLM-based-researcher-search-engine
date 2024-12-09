from aiLib import AILib
import os
from embeddingsVectors import EmbeddingVectors

gpt = AILib(
    api_key=os.environ["OPENAI_API_KEY"],
    api_version="2024-02-01",
    azure_endpoint="https://tu-openai-api-management.azure-api.net/oltatkull/openai/deployments/IDS2024_MATETSKI_gpt_4o_mini/chat/completions?api-version=2024-02-01"
)

embedding_vectors = EmbeddingVectors(
    api_key=os.environ["OPENAI_API_KEY"],
    api_version="2024-02-01",
    azure_endpoint="https://tu-openai-api-management.azure-api.net/oltatkull/openai/deployments/IDS2024_MATETSKI_EMBEDDING/embeddings?api-version=2024-02-01"
)


class Service:
    def __init__(self):
        pass

    def processPrompt(self, user_prompt):
        print(f"User prompt: {user_prompt}")
        prompt = gpt.extract(user_prompt)
        print(f"Prompt: {prompt}")
        return embedding_vectors.getNearestEmbedding(prompt, n=5)

