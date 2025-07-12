import weaviate
from weaviate.classes.init import Auth
from weaviate.classes.config import Configure
import os

# Best practice: store your credentials in environment variables
weaviate_url = os.environ["WEAVIATE_URL"]
weaviate_api_key = os.environ["WEAVIATE_API_KEY"]

print(f"Connecting to: {weaviate_url!r}")

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=weaviate_url,
    auth_credentials=Auth.api_key(weaviate_api_key),
)

questions = client.collections.create(
    name="Question",
    vectorizer_config=Configure.Vectorizer.text2vec_weaviate(),
    generative_config=Configure.Generative.cohere()
)

print(client.is_ready())  # Should print: `True`

client.close()  # Free up resources