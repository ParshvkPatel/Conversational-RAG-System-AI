# 📚 Conversational RAG System

An AI-powered Conversational Retrieval-Augmented Generation (RAG) system built using Gujarat State School Textbooks (GSSTB). The application answers user questions strictly from the provided textbooks using semantic search and Large Language Models (LLMs).

---

## 🚀 Features

- 📄 Supports 400+ Gujarat State School Textbooks
- 📚 Answers only from textbook content
- 💬 Conversational Chat Interface
- 🧠 Context-Aware Retrieval
- 🔍 FAISS Vector Database
- 🤖 Groq Llama 3.3 70B Integration
- 📖 Displays textbook source and page number
- ⚡ Fast semantic search using BAAI/bge-small-en-v1.5 embeddings
- 🎯 Subject-aware retrieval
- 📝 Chat history support

---

## 📂 Dataset

- **Total PDFs:** 406
- **Total Pages:** 13,353
- **Total Chunks:** 30,628

Source:
Gujarat State School Textbook Board (GSSTB)

---

## 🏗️ Project Structure

```
Conversational-RAG-System/
│
├── data/
├── vector_db/
├── app.py
├── rag.py
├── llm.py
├── embedding.py
├── chunking.py
├── extraction.py
├── prompts.py
├── documents.json
├── chunks.json
├── requirements.txt
├── .env
└── README.md
```

---

## ⚙️ Technologies Used

- Python
- Streamlit
- LangChain
- FAISS
- HuggingFace Embeddings
- Groq API
- Llama 3.3 70B
- PyMuPDF
- JSON

---

## 🛠️ Installation

### Clone Repository

```bash
git clone https://github.com/ParshvkPatel/Conversational-RAG-System.git
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Create Environment File

```
GROQ_API_KEY=YOUR_API_KEY
```

### Generate Embeddings

```bash
python embedding.py
```

### Run Streamlit App

```bash
streamlit run app.py
```

---

## 💬 Example Questions

- What is Photosynthesis?
- Explain Democracy.
- What is Newton's First Law?
- What is Cell?
- Define Constitution.

---

## 📖 Example Output

Question:

```
What is Photosynthesis?
```

Answer:

```
Photosynthesis is the process by which green plants use sunlight to prepare food.
```

Source:

```
Biology
Std 11
Page 144
```

---

## 📸 Screenshots

Add screenshots inside the `screenshots/` folder.

Example:

```
screenshots/
    home.png
    chat.png
    answer.png
```

---

## 🔮 Future Improvements

- Multi-language support
- PDF Upload
- Voice Assistant
- OCR Support
- Hybrid Search
- Citation Highlighting

---

## 👨‍💻 Author

**Parshv Patel**

B.Tech Information Technology

Silver Oak University

GitHub:
https://github.com/ParshvkPatel

---

## ⭐ If you like this project, don't forget to star the repository.