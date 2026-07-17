import json
import os
import shutil

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# ==========================================================
# Configuration
# ==========================================================

CHUNKS_FILE = "chunks.json"
VECTOR_DB = "vector_db"

BATCH_SIZE = 500


print("=" * 70)
print("FAISS Embedding Pipeline Started")
print("=" * 70)


# ==========================================================
# Load Chunks
# ==========================================================

with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
    chunks = json.load(f)


print(f"Total Chunks Loaded : {len(chunks)}")


# ==========================================================
# Load Embedding Model
# ==========================================================

print("\nLoading Embedding Model...")

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",
    model_kwargs={
        "device": "cpu"
    },
    encode_kwargs={
        "normalize_embeddings": True,
        "batch_size": 32
    }
)


print("Embedding Model Loaded")


# ==========================================================
# Remove Old Vector DB
# ==========================================================

if os.path.exists(VECTOR_DB):

    print("\nRemoving Old Vector Database...")

    shutil.rmtree(VECTOR_DB)



# ==========================================================
# Create FAISS Index
# ==========================================================


db = None


print("\nCreating FAISS Index...\n")


for start in range(0, len(chunks), BATCH_SIZE):


    end = min(
        start + BATCH_SIZE,
        len(chunks)
    )


    batch = chunks[start:end]


    documents = []


    for item in batch:


        documents.append(

            Document(

                page_content=item["text"],


                metadata={

                    "chunk_id":
                    item.get("chunk_id"),


                    "document_id":
                    item.get("document_id"),


                    "language":
                    item.get("language"),


                    "standard":
                    item.get("standard"),


                    "subject":
                    item.get(
                        "subject",
                        "Unknown"
                    ),


                    "book_name":
                    item.get(
                        "book_name",
                        ""
                    ),


                    "source":
                    item.get(
                        "source"
                    ),


                    "page":
                    item.get(
                        "page"
                    )

                }

            )

        )



    if db is None:


        db = FAISS.from_documents(
            documents,
            embeddings
        )


    else:


        db.add_documents(
            documents
        )



    print(
        f"Processed {end}/{len(chunks)} chunks"
    )



# ==========================================================
# Save Database
# ==========================================================


os.makedirs(
    VECTOR_DB,
    exist_ok=True
)


db.save_local(
    VECTOR_DB
)



print("\n")
print("=" * 70)
print("FAISS DATABASE CREATED SUCCESSFULLY")
print("=" * 70)

print(
    f"Total Vectors : {db.index.ntotal}"
)

print(
    f"Saved At      : {VECTOR_DB}"
)

print("=" * 70)