from garuddb import PersistentClient

DB_PATH = "./garud_db"
COLLECTION_NAME = "gleif_rr"

client = PersistentClient(DB_PATH)
collection = client.get_collection(COLLECTION_NAME)

queries = [
    "fund managed by another entity",
    "ultimate parent company",
    "direct parent company",
    "sub fund",
    "active relationship",
    "entity consolidation",
    "investment fund",
    "subsidiary company"
]

for query in queries:

    print("\n" + "=" * 100)
    print(f"QUERY: {query}")
    print("=" * 100)

    results = collection.query(
        query_texts=[query],
        n_results=5
    )

    ids = results["ids"][0]
    docs = results["documents"][0]
    distances = results["distances"][0]

    for i in range(len(ids)):
        print(f"\nResult #{i+1}")
        print(f"ID       : {ids[i]}")
        print(f"Distance : {distances[i]:.4f}")
        print(docs[i])