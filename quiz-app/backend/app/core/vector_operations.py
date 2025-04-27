import torch
from weaviate.classes.config import Property, DataType
from weaviate.exceptions import WeaviateBaseError
from transformers import AutoModel
from core.config.weaviate_config import WeaviateConfig
import redis
import json

redis_client = redis.Redis(host="localhost", port=6379, db=0)


class VectorDBOperations:
    @staticmethod
    def connect_weaviate():
        return WeaviateConfig.connect_()

    @staticmethod
    def create_schema(client, class_name):
        try:
            client.collections.create(
                class_name,
                properties=[
                    Property(name="content", data_type=DataType.TEXT),
                    Property(name="chunk_index", data_type=DataType.INT),
                    Property(name="user_id", data_type=DataType.TEXT),
                    Property(name="pdf_id", data_type=DataType.TEXT),
                ],
            )
            print(f"Schema created for class '{class_name}'")
        except WeaviateBaseError as e:
            print(e)

    @staticmethod
    def insert(client, chunks, user_id):
        try:
            if not client.collections.exists(user_id):
                VectorDBOperations.create_schema(client, user_id)

            embedding_model = AutoModel.from_pretrained(
                "./model/ml_model", trust_remote_code=True
            )

            pdf_chunk = client.collections.get(user_id)
            n = len(chunks)
            for index, chunk in enumerate(chunks):
                progress = index/n * 100
                print("progress:",progress)
                redis_client.publish(user_id, json.dumps({"progress": f"{progress:.2f}"}))
                device = "cuda" if torch.cuda.is_available() else "cpu"
                embedding = embedding_model.encode(chunk[0],device=device)

                metadata = {
                    "content": chunk,
                    "chunk_index": index,
                    "pdf_id": chunk[1],
                }

                uuid = pdf_chunk.data.insert(metadata, vector=embedding)

            print("All chunks saved successfully!", uuid)
            redis_client.publish(user_id,json.dumps({"progress":"100.00"}))
        except WeaviateBaseError as e:
            print("hello")
            print(e)

    @staticmethod
    def read(client, class_name):
        try:
            return client.collections.get(class_name)
        except WeaviateBaseError as e:
            print(e)

    @staticmethod
    def delete(client, class_name):
        print("deleting began...")
        try:
            client.collections.delete(class_name)
            print("deleting done...")
        except WeaviateBaseError as e:
            print(e)


if "__main__" == __name__:
    client = VectorDBOperations.connect_weaviate()
    VectorDBOperations.delete(client, "pdf_chunk")
