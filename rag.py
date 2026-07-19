from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from llm import generate_answer

# ==========================================================
# Load Embedding Model
# ==========================================================

print("Loading Embedding Model...")

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)

# ==========================================================
# Load FAISS Database
# ==========================================================

print("Loading FAISS Database...")

db = FAISS.load_local(
    "vector_db",
    embeddings,
    allow_dangerous_deserialization=True
)

print("\n✅ Conversational RAG Ready")
print("Type 'exit' to quit.\n")

# ==========================================================
# Better Retriever (MMR)
# ==========================================================

retriever = db.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 4,
        "fetch_k": 15
    }
)

# ==========================================================
# Subject Detection
# ==========================================================

def detect_subject(question):

    q = question.lower()

    mapping = {

        "biology": [
            "photosynthesis", "cell", "plant", "animal",
            "respiration", "dna", "rna", "blood",
            "heart", "human", "leaf", "chlorophyll"
        ],

        "physics": [
            "force", "motion", "electricity", "current",
            "voltage", "magnet", "light",
            "reflection", "refraction",
            "gravity", "newton"
        ],

        "chemistry": [
            "acid", "base", "salt",
            "atom", "molecule",
            "reaction", "chemical",
            "compound", "element"
        ],

        "mathematics": [
            "triangle", "algebra",
            "geometry", "circle",
            "equation", "graph",
            "trigonometry",
            "probability",
            "statistics",
            "matrix",
            "calculus"
        ],

        "political science": [
            "democracy",
            "constitution",
            "government",
            "parliament",
            "rights",
            "citizen",
            "election"
        ],

        "history": [
            "freedom",
            "independence",
            "gandhi",
            "british",
            "mughal",
            "ashoka"
        ],

        "geography": [
            "river",
            "mountain",
            "climate",
            "soil",
            "earthquake",
            "volcano",
            "plateau",
            "map"
        ]
    }

    for subject, words in mapping.items():

        for word in words:

            if word in q:

                return subject

    return None
# ==========================================
# Conversation History
# ==========================================

chat_history = []

# ==========================================================
# Chat Loop
# ==========================================================

while True:

    question = input("\nQuestion : ")

    if question.lower() == "exit":
        print("\nGoodbye 👋")
        break

    subject = detect_subject(question)

    if subject:

        docs = retriever.invoke(
            f"{subject} {question}"
        )

    else:

        docs = retriever.invoke(question)
        
    history = ""

# Keep only last 3 conversations

    for q, a in chat_history[-3:]:

        history += f"User: {q}\n"

        history += f"Assistant: {a}\n\n"    
    # Build Context

    context = ""

    for d in docs:

        context += f"""

Book : {d.metadata.get('book_name','')}

Subject : {d.metadata.get('subject','Unknown')}

Standard : {d.metadata.get('standard','')}

Language : {d.metadata.get('language','')}

Page : {d.metadata.get('page','')}

Content:
{d.page_content}

--------------------------------------------------

"""
# Add Conversation History

    context = f"""
    Conversation History

    {history}

    Retrieved Text

    {context}
"""
    # Generate Answer
    print("\nGenerating Answer...")
    answer = generate_answer(
        question,
        context
    )
    if len(docs) == 0:

        print("No relevant textbook found.")

    continue

    chat_history.append(
    (
        question,
        answer
    )
)
    print("Answer Generated")

    print("\n" + "=" * 80)

    print(answer)

    print("=" * 80)

    print("\nRetrieved Sources\n")

seen = set()

count = 1

for d in docs:

    key = (
        d.metadata["source"],
        d.metadata["page"]
    )

    if key in seen:
        continue

    seen.add(key)

    print(
        f"{count}. "
        f"{d.metadata.get('subject','Unknown')} | "
        f"{d.metadata.get('book_name','')} | "
        f"{d.metadata.get('source','')} | "
        f"Page {d.metadata.get('page','')}"
    )

    count += 1