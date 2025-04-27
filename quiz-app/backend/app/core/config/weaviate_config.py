from .settings import settings
from weaviate.classes.init import AdditionalConfig, Timeout
from weaviate.classes.init import Auth
import weaviate

class WeaviateConfig:
    @staticmethod
    def connect_():
        weaviate_url = settings.WEAVIATE_URL
        weaviate_api_key = settings.WEAVIATE_API_KEY
        print(weaviate_api_key, weaviate_url)
        client = weaviate.connect_to_weaviate_cloud(
            cluster_url=weaviate_url,
            auth_credentials=Auth.api_key(weaviate_api_key),
            additional_config=AdditionalConfig(
                timeout=Timeout(init=300, query=60, insert=120)  # Values in seconds
            ),
        )
        return client