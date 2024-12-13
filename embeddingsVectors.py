# embeddingsVectors.py
from openai import AzureOpenAI
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility, Index


def _initialize_collection():
    collection_name = "embeddings"
    if utility.has_collection(collection_name):
        pass
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="authors", dtype=DataType.VARCHAR, max_length=3102),
        FieldSchema(name="title", dtype=DataType.VARCHAR, max_length=3102),
        # FieldSchema(name="link", dtype=DataType.VARCHAR, max_length=3102),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=1536),
    ]
    schema = CollectionSchema(fields, "Embedding collection schema")
    collection = Collection(collection_name, schema)
    return collection


def _connect_to_milvus():
    connections.connect(
        alias="default",
        host="localhost",
        port="19530"
    )


class EmbeddingVectors:
    def __init__(self, api_key, api_version, azure_endpoint):
        self.client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=azure_endpoint
        )
        # Establish connection to Milvus
        _connect_to_milvus()
        # Initialize the Milvus collection with the expected schema
        self.collection = _initialize_collection()
        # Create an index on the embedding field
        index_params = {"index_type": "IVF_FLAT", "params": {"nlist": 128}, "metric_type": "L2"}
        self.collection.create_index(field_name="embedding", index_params=index_params)

    def insert_embeddings(self, df):
        """
        Insert the embeddings into the Milvus collection.
        """
        embeddings = df["combined"].apply(self.extract).tolist()
        authors = df["Authors"].tolist()
        titles = df["Title"].tolist()
        # links = df["Link"].tolist()

        data = [authors, titles, embeddings]  # Prepare the data to match the schema
        self.collection.insert(data)

    def extract(self, text):
        """
        Extract the embedding from the text.
        """
        embedding_response = self.client.embeddings.create(
            model="IDS2024_MATETSKI_EMBEDDING",
            input=text
        )
        return embedding_response.data[0].embedding

    def getNearestEmbedding(self, specific_text, n=1):
        """
        Get the nearest embeddings to the specific text.
        """
        self.collection.load()
        specific_embedding = self.extract(specific_text)
        search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
        results = self.collection.search(
            data=[specific_embedding],
            anns_field="embedding",
            param=search_params,
            limit=n,
            expr=None,
            output_fields=["authors", "title"]
        )
        return [(result.entity.get("authors"), result.entity.get("title")) for result in results[0]]
