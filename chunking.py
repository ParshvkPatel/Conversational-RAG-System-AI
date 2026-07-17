import json
import re
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ==========================================
# Load Documents
# ==========================================

with open("documents.json", "r", encoding="utf-8") as f:
    documents = json.load(f)

print("=" * 60)
print(f"Loaded Pages : {len(documents)}")
print("=" * 60)

# ==========================================
# Chunk Configuration
# ==========================================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150,
    separators=[
        "\n\n",
        "\n",
        ". ",
        "? ",
        "! ",
        "; ",
        ", ",
        " ",
        ""
    ]
)

# ==========================================
# Subject Detection
# ==========================================

def detect_subject(filename):

    name = filename.lower()

    subject_map = {

        "math": "Mathematics",
        "mathematics": "Mathematics",

        "science": "Science",

        "biology": "Biology",
        "physics": "Physics",
        "chemistry": "Chemistry",

        "social": "Social Science",
        "history": "History",
        "geography": "Geography",
        "political": "Political Science",
        "economics": "Economics",

        "english": "English",
        "beehive": "English",
        "kaleidoscope": "English",
        "hornbill": "English",
        "flamingo": "English",

        "hindi": "Hindi",
        "gujarati": "Gujarati",

        "computer": "Computer",
        "informatics": "Computer",
        "it": "Information Technology"
    }

    for key, value in subject_map.items():
        if key in name:
            return value

    return "Unknown"

# ==========================================
# Book Name Extraction
# ==========================================

def extract_book_name(filename):

    name = Path(filename).stem

    name = re.sub(r"Std[-_ ]?\d+", "", name, flags=re.IGNORECASE)

    name = re.sub(r"English.?Medium", "", name, flags=re.IGNORECASE)
    name = re.sub(r"Gujarati.?Medium", "", name, flags=re.IGNORECASE)
    name = re.sub(r"Hindi.?Medium", "", name, flags=re.IGNORECASE)

    name = name.replace("_", " ").replace("-", " ")

    return name.strip()

# ==========================================
# Create Chunks
# ==========================================

chunks = []
chunk_counter = 1

seen = set()

for doc in documents:

    splits = text_splitter.split_text(doc["text"])

    for chunk in splits:

        chunk = chunk.strip()

        if len(chunk) < 40:
            continue

        key = (
            doc["source"],
            doc["page"],
            chunk
        )

        if key in seen:
            continue

        seen.add(key)

        metadata = {

            "chunk_id": chunk_counter,

            "language": doc["language"],

            "standard": doc["standard"],

            "subject": detect_subject(doc["source"]),

            "book_name": extract_book_name(doc["source"]),

            "source": doc["source"],

            "page": doc["page"],

            "text": chunk

        }

        chunks.append(metadata)

        chunk_counter += 1

# ==========================================
# Save JSON
# ==========================================

with open("chunks.json", "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=2, ensure_ascii=False)

print("=" * 60)
print(f"Total Pages   : {len(documents)}")
print(f"Total Chunks  : {len(chunks)}")
print("Saved File    : chunks.json")
print("=" * 60)

print("\nSample Chunk:\n")
print(json.dumps(chunks[0], indent=2, ensure_ascii=False))