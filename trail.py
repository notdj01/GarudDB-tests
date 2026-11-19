from garuddb import PersistentClient
from pprint import pprint

DB_PATH = "./garud_db"
COLLECTION_NAME = "gleif_rr"

client = PersistentClient(DB_PATH)

print("Collections:")
print(client.list_collections())

collection = client.get_collection(COLLECTION_NAME)

print("\nDocument Count:")
print(collection.count())

print("\nFirst 5 Documents:")

results = collection.get(
    ids=["0", "1", "2", "3", "4"]
)

for i in range(len(results["ids"])):
    print("=" * 70)
    print("ID:", results["ids"][i])
    print(results["documents"][i])