from garuddb import PersistentClient

client = PersistentClient("./garud_db")
collection = client.get_collection("gleif_rr")

results = collection.query(
    query_texts=[
        "investment funds managed by BlackRock"
    ],
    n_results=5
)

print(results)