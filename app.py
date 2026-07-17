# import streamlit as st

# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_community.vectorstores import FAISS

# from llm import generate_answer


# # ==========================================
# # Page Config
# # ==========================================

# st.set_page_config(
#     page_title="Conversational RAG",
#     page_icon="📚",
#     layout="wide"
# )

# st.title("📚 Conversational RAG System")
# st.write("Ask questions from Gujarat State School Textbooks")


# # ==========================================
# # Load Vector DB
# # ==========================================

# @st.cache_resource
# def load_db():

#     embeddings = HuggingFaceEmbeddings(
#         model_name="BAAI/bge-small-en-v1.5"
#     )

#     db = FAISS.load_local(
#         "vector_db",
#         embeddings,
#         allow_dangerous_deserialization=True
#     )

#     return db


# db = load_db()


# # ==========================================
# # Subject Detection
# # ==========================================

# def detect_subject(question):

#     q = question.lower()

#     mapping = {

#         "biology":[
#             "photosynthesis","cell","plant","animal","respiration",
#             "dna","rna","blood","heart","human","leaf","chlorophyll"
#         ],

#         "physics":[
#             "force","motion","electricity","current",
#             "voltage","magnet","light","gravity"
#         ],

#         "chemistry":[
#             "acid","base","salt","atom",
#             "molecule","reaction","chemical"
#         ],

#         "mathematics":[
#             "triangle","algebra","geometry",
#             "circle","equation","graph"
#         ],

#         "political science":[
#             "democracy","constitution",
#             "government","rights","citizen"
#         ],

#         "history":[
#             "gandhi","ashoka","mughal",
#             "history","british","freedom"
#         ],

#         "geography":[
#             "river","mountain","soil",
#             "climate","plateau","earthquake"
#         ]

#     }

#     for subject, words in mapping.items():

#         for word in words:

#             if word in q:

#                 return subject

#     return None


# # ==========================================
# # Chat History
# # ==========================================

# if "messages" not in st.session_state:
#     st.session_state.messages = []


# for msg in st.session_state.messages:

#     with st.chat_message(msg["role"]):

#         st.markdown(msg["content"])


# # ==========================================
# # User Question
# # ==========================================

# question = st.chat_input("Ask your question...")


# if question:

#     st.session_state.messages.append(
#         {
#             "role":"user",
#             "content":question
#         }
#     )

#     with st.chat_message("user"):

#         st.markdown(question)

#     with st.spinner("Searching textbooks..."):

#         subject = detect_subject(question)

#         retriever = db.as_retriever(
#             search_type="mmr",
#             search_kwargs={
#                 "k":5,
#                 "fetch_k":15
#             }
#         )

#         if subject:

#             docs = retriever.invoke(
#                 f"{subject} {question}"
#             )

#         else:

#             docs = retriever.invoke(question)


#         context = "\n\n".join(

#             [

#                 f"""
# Book : {d.metadata.get("book_name","")}

# Subject : {d.metadata.get("subject","Unknown")}

# Standard : {d.metadata.get("standard","")}

# Language : {d.metadata.get("language","")}

# Page : {d.metadata.get("page","")}

# Content:
# {d.page_content}
# """

#                 for d in docs

#             ]

#         )

#         answer = generate_answer(
#             question,
#             context
#         )

#     with st.chat_message("assistant"):

#         st.markdown(answer)

#         st.markdown("---")

#         st.subheader("📖 Sources")

#         for d in docs:

#             st.write(
#                 f"**{d.metadata.get('book_name','')}** | "
#                 f"{d.metadata.get('subject','Unknown')} | "
#                 f"Std {d.metadata.get('standard','')} | "
#                 f"Page {d.metadata.get('page','')}"
#             )

#     st.session_state.messages.append(
#         {
#             "role":"assistant",
#             "content":answer
#         }
#     )
import streamlit as st

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


st.title("📚 Conversational RAG System")

st.caption(
    "AI Assistant for Gujarat State School Textbook Board (GSSTB)"
)


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



# ==========================================
# Session Memory
# ==========================================

if "messages" not in st.session_state:

    st.session_state.messages = []



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
    "Ask your textbook question..."
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



            retriever = db.as_retriever(
             search_type="similarity_score_threshold",
             search_kwargs={
                "k":3,
            "score_threshold":0.5
            }
        )



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
                    f"Std {d.metadata.get('standard','')} | "
                    f"Page {d.metadata.get('page','')}"

                    )


                    if source not in seen:

                        sources.append(source)

                        seen.add(source)



        st.markdown(answer)



        if sources and "not available" not in answer.lower():

            with st.expander(
                "📖 Textbook Sources"
            ):

                for s in sources:

                    st.write(
                        "• " + s
                    )



    st.session_state.messages.append(

        {
            "role":"assistant",
            "content":answer,
            "sources":sources
        }

    )