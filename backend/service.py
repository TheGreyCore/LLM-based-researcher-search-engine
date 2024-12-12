from aiLib import AILib
import os
import logging
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

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Service:
    def __init__(self):
        pass

    def processPrompt(self, user_prompt):
        """
        Process user prompt and return the result of searching in human-readable form.
        """
        logging.info(f"Prompt: {user_prompt}")
        response = gpt.extract(user_prompt)
        logging.info(f"Prompt: {response}")
        if response.startswith("[ERROR]"):
            return "Invalid search query. We can not help you with that :("
        n = int(response.split("]")[0].split("=")[1])
        prompt = response.split("]")[1].strip()
        unprocessed_output = embedding_vectors.getNearestEmbedding(prompt, n=n)
        return gpt.create_output(user_prompt, unprocessed_output)
