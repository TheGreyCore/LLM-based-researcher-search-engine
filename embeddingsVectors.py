from openai import AzureOpenAI


class EmbeddingVectors:
    def __init__(self, api_key, api_version, azure_endpoint):
        self.client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=azure_endpoint
        )

    def extract(self, text):
        """
        Extract embeddings from text.
        Returns: embedding vector in string format.
        """
        embedding_response = self.client.embeddings.create(
            model="IDS2024_MATETSKI_EMBEDDING",
            input=text
        )
        return embedding_response.data[0].embedding



