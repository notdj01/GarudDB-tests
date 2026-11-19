import pandas as pd

from garuddb import PersistentClient, DefaultEmbeddingFunction

# ==========================================================
# CONFIGURATION
# ==========================================================

CSV_PATH = "20260806-0800-gleif-goldencopy-rr-golden-copy.csv"   # <-- Your extracted CSV

DB_PATH = "./garud_db"

COLLECTION_NAME = "gleif_rr"

CHUNK_SIZE = 5000
BATCH_SIZE = 500

# ==========================================================
# CONNECT TO GARUDDB
# ==========================================================

client = PersistentClient(DB_PATH)

collection = client.get_or_create_collection(
    COLLECTION_NAME,
    embedding_function=DefaultEmbeddingFunction()
)

# ==========================================================
# BUILD SEARCHABLE DOCUMENT
# ==========================================================

def row_to_document(row):
    return (
        f"Relationship Type: {row['Relationship.RelationshipType']}\n"
        f"Start LEI: {row['Relationship.StartNode.NodeID']}\n"
        f"End LEI: {row['Relationship.EndNode.NodeID']}\n"
        f"Relationship Status: {row['Relationship.RelationshipStatus']}\n"
        f"Registration Status: {row['Registration.RegistrationStatus']}\n"
        f"Managing LOU: {row['Registration.ManagingLOU']}"
    )

# ==========================================================
# INGEST CSV
# ==========================================================

total = 0

reader = pd.read_csv(
    CSV_PATH,
    chunksize=CHUNK_SIZE,
    dtype=str,
    keep_default_na=False
)

for chunk in reader:

    ids = []
    documents = []
    metadatas = []

    for _, row in chunk.iterrows():

        ids.append(str(total))
        documents.append(row_to_document(row))
        metadatas.append(row.to_dict())

        total += 1

        if len(ids) >= BATCH_SIZE:

            collection.add(
                ids=ids,
                documents=documents,
                metadatas=metadatas
            )

            print(f"Inserted {total:,} rows")

            ids = []
            documents = []
            metadatas = []

    if ids:
        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )

        print(f"Inserted {total:,} rows")

print(f"\nFinished! Total rows inserted: {total:,}")