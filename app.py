import streamlit as st

# ==========================================
# Custom CSS
# ==========================================

st.markdown("""
<style>

.main{
    background-color:#f5f7fb;
}

h1{
    color:#0F172A;
    font-weight:700;
}

.stChatMessage{
    border-radius:15px;
    padding:15px;
    margin-bottom:10px;
}

.stButton>button{
    width:100%;
    border-radius:10px;
    background:#2563EB;
    color:white;
    font-weight:bold;
}

.stButton>button:hover{
    background:#1D4ED8;
}

[data-testid="stSidebar"]{
    background:#111827;
}

[data-testid="stSidebar"] *{
    color:white;
}

.stExpander{
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from llm import generate_answer


# ==========================================
# Page Config
# ==========================================

st.set_page_config(
    page_title="Conversational RAG System",
    page_icon="📚",
    layout="wide"
)
# ==========================================
# Chat History
# ==========================================

if "messages" not in st.session_state:

    st.session_state.messages = []

st.markdown("""
<h1 style='font-size:52px; font-weight:bold; margin-bottom:0;'>
📚 Conversational RAG System
</h1>
<h3 style='font-size:24px; font-weight:400; color:#bdbdbd; margin-top:5px;'>
AI Assistant for Gujarat State School Textbooks
</h3>
""", unsafe_allow_html=True)
# ==========================================
# Sidebar
# ==========================================

with st.sidebar:

    st.markdown ("""
📚 Conversational RAG System

AI Assistant for Gujarat State School Textbooks
                    """)                

    st.markdown("---")

    st.write("### Dataset")

    st.write("📄 PDFs : 406")

    st.write("📑 Pages : 13,353")

    st.write("🧩 Chunks : 30,628")

    st.write("🤖 LLM : Llama 3.3 70B")
    st.markdown("---")

    st.write("### Session")

    st.metric(
    "Messages",
    len(st.session_state.messages)
)

    st.write("🔎 Embedding : BAAI/bge-small-en-v1.5")

    st.markdown("---")

    if st.button("🗑️ Clear Chat"):

        st.session_state.messages = []

        st.rerun()


# ==========================================
# Load Vector DB
# ==========================================

@st.cache_resource
def load_db():

    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-en-v1.5"
    )

    db = FAISS.load_local(
        "vector_db",
        embeddings,
        allow_dangerous_deserialization=True
    )

    return db


db = load_db()
# ==========================================
# Retriever
# ==========================================

retriever = db.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={
        "k": 5,
        "score_threshold": 0.5
    }
)

# ==========================================
# Welcome Message
# ==========================================

if len(st.session_state.messages) == 0:

    st.info("""
👋 Welcome

Ask questions from Gujarat State School Textbooks.

Examples:
• What is Photosynthesis?
• Explain Democracy.
• Newton's First Law
""")

# ==========================================
# Subject Detection
# ==========================================

def detect_subject(question):

    q = question.lower()

    mapping = {

        "biology":[
            "photosynthesis",
            "cell",
            "plant",
            "dna",
            "rna",
            "human"
        ],

        "physics":[
            "force",
            "motion",
            "electricity",
            "light"
        ],

        "chemistry":[
            "acid",
            "base",
            "atom",
            "reaction"
        ],

        "mathematics":[
            "triangle",
            "equation",
            "algebra"
        ]

    }


    for subject, words in mapping.items():

        for word in words:

            if word in q:
                return subject


    return None

# Display Chat

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])


        if "sources" in msg:

            with st.expander("📖 View Sources"):

                for source in msg["sources"]:
                    st.write(source)



# ==========================================
# Question Input
# ==========================================


question = st.chat_input(
    "Ask anything from the textbooks..."
)



if question:


    st.session_state.messages.append(
        {
            "role":"user",
            "content":question
        }
    )


    with st.chat_message("user"):

        st.markdown(question)



    with st.chat_message("assistant"):


        with st.spinner(
            "🔍 Searching textbooks..."
        ):


            subject = detect_subject(question)

            if subject:

                docs = retriever.invoke(
                    f"{subject} {question}"
                )

            else:

                docs = retriever.invoke(
                    question
                )



            if not docs:

                answer = (
                    "Sorry, this information is not "
                    "available in the provided textbooks."
                )

                sources=[]


            else:
                history = ""

                for msg in st.session_state.messages[-6:]:

                         role = "User" if msg["role"] == "user" else "Assistant"

                         history += f"{role}: {msg['content']}\n"


                context="\n\n".join(

                    [

                    f"""
Book:{d.metadata.get('book_name')}

Subject:{d.metadata.get('subject')}

Standard:{d.metadata.get('standard')}

Page:{d.metadata.get('page')}

Content:
{d.page_content}

"""

                    for d in docs

                    ]

                )
                context = f"""  
                    Conversation History

                {history}

                Retrieved Text

                {context}
                """

                answer = generate_answer(
                    question,
                    context
                )



                sources=[]


                seen=set()


                for d in docs:


                    source=(

                    f"{d.metadata.get('book_name','')} | "
                    f"{d.metadata.get('subject','')} | "
                    f"{d.metadata.get('standard','').replace('_',' ')} | "
                    f"Page {d.metadata.get('page','')}"

                    )


                    if source not in seen:

                        sources.append(source)

                        seen.add(source)



        st.subheader("📖 Answer")

        st.write(answer)


        if sources and "not available" not in answer.lower():

            with st.expander(
                "📖 Textbook Sources"
            ):

                for s in sources:

                    st.success(s)


    st.session_state.messages.append(

        {
            "role":"assistant",
            "content":answer,
            "sources":sources
        }

    )
  # ==========================================
# Download Chat
# ==========================================

chat_text = ""

for msg in st.session_state.messages:

    role = "User" if msg["role"] == "user" else "Assistant"

    chat_text += f"{role}\n"
    chat_text += f"{msg['content']}\n\n"


if st.session_state.messages:

    st.download_button(
        label="📥 Download Chat",
        data=chat_text,
        file_name="conversation.txt",
        mime="text/plain",
        key="download_chat_button"
    )


st.markdown("---")

st.markdown(
"""
<center>

Developed ❤️ by <b>Parshv Patel</b>

Conversational RAG System

Gujarat State School Textbooks

</center>
""",
unsafe_allow_html=True
)