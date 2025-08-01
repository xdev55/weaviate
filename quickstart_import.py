import weaviate
from weaviate.classes.init import Auth
import requests, json, os

weaviate_url = os.environ["WEAVIATE_URL"]
weaviate_api_key = os.environ["WEAVIATE_API_KEY"]


client = weaviate.connect_to_weaviate_cloud(
    cluster_url=weaviate_url,
    auth_credentials=Auth.api_key(weaviate_api_key),
)

resp = requests.get(
    "https://raw.githubusercontent.com/weaviate-tutorials/quickstart/main/data/jeopardy_tiny.json"
)

data = json.loads(resp.text)

questions = client.collections.get("Question")

with questions.batch.fixed_size(batch_size=200) as batch:
    for d in data:
        batch.add_object(
            {
                "answer": d["Answer"],
                "question": d["Question"],
                "category": d["Category"],
            }
        )
        if batch.number_errors > 10:
            print("Batch import stopped due to excessive errors.")
            break

failed_objects = questions.batch.failed_objects
if failed_objects:
    print(f"Number of failed imports: {len(failed_objects)}")
    print(f"First failed object: {failed_objects[0]}")

client.close()