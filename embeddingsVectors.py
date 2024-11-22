from openai import AzureOpenAI
from codecs import encode
from scipy.spatial.distance import cosine


def getCosineSimilarity(embedding1, embedding2):
    """
    Get cosine similarity between two embeddings.
    """
    return cosine(embedding1, embedding2)


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

    def getEmbeddingsVectorsFromCSV(self, combined_df, max_tokens=8000,
                                    save_path="publications_extraction_test_data.csv"):
        """
        Extract embeddings from combined_df. Save the results to save_path. DF should have a column named "combined" and
        the text to be embedded should be in that column.
        """
        combined_df["n_tokens"] = combined_df.combined.apply(lambda x: len(encode(str(x), "utf-8")))
        df = combined_df[combined_df.n_tokens <= max_tokens]

        df["embedding"] = df.combined.apply(lambda x: self.extract(x))
        df.to_csv(save_path)

    def getNearestEmbedding(self, df, specific_embedding, n=3):
        """
        Find the nearest embedding vector using cosine similarity.
        """
        product_embedding = self.extract(specific_embedding)
        df["similarity"] = df.embedding.apply(lambda x: getCosineSimilarity(x, product_embedding))

        results = (
            df.sort_values("similarity", ascending=True)
            .head(n)
            .combined.str.replace("Title: ", "")
            .str.replace("; Content:", ": ")
        )

        return results
