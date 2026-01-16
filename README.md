# Langchain Chatbot Guide for Catastrophe Preparation
---

# 🛡️ Catastrophe Preparation Guide Chatbot

An AI-powered assistant designed to provide accurate emergency preparedness advice based on official guidance from the **BBK (Bundesamt für Bevölkerungsschutz und Katastrophenhilfe)**.

[Link to PDF Source](https://www.bbk.bund.de/SharedDocs/Downloads/DE/Mediathek/Publikationen/Buergerinformationen/Ratgeber/BBK-Vorsorgen-fuer-Krisen-und-Katastrophen.pdf?__blob=publicationFile&v=41)

This application uses **Retrieval-Augmented Generation (RAG)** to ensure that the chatbot only answers based on provided official PDF documents, preventing "hallucinations" and ensuring high-quality safety information.

## 🚀 Features

* **Local Privacy:** Runs entirely on your local machine using **Ollama**. No data is sent to external APIs (OpenAI, Google, etc.).
* **Context-Aware:** Uses the official BBK "Ratgeber für Notfallvorsorge" as its primary knowledge base.
* **Semantic Search:** Utilizes **FAISS** and high-performance embeddings to find specific sections in PDFs (like water storage, food supply, or medical kits).
* **Streamlit Interface:** A clean, chat-based user interface for easy interaction.

## 🛠️ Tech Stack

* **LLM:** [Gemma:2b](https://ollama.com/library/gemma) (via Ollama)
* **Embeddings:** [mxbai-embed-large](https://ollama.com/library/mxbai-embed-large) (via Ollama)
* **Framework:** LangChain
* **Vector Store:** FAISS
* **UI:** Streamlit

## 📋 Prerequisites

Before running the app, you must have **Ollama** installed and the necessary models pulled.

1. **Install Ollama:** [Download here](https://ollama.com/)
2. **Pull the Models:**
```bash
ollama pull gemma:2b
ollama pull mxbai-embed-large

```



## ⚙️ Installation & Setup

1. **Clone the Repository:**
```bash
git clone https://github.com/iceyisaak/langchain-chatbot-guide-for-catastrophe-preparation.git
cd langchain-chatbot-guide-for-catastrophe-preparation

```


2. **Create a Virtual Environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

```


3. **Install Dependencies:**
```bash
pip install -r requirements.txt

```


4. **Prepare Documents:**
* Create a folder named `document/` in the root directory.
* Place your BBK PDFs (or any other preparedness PDFs) inside this folder.


5. **Run the Application:**
```bash
streamlit run app.py

```



## 📖 How it Works

1. **Ingestion:** The app reads all PDFs in the `./document` folder.
2. **Chunking:** The text is split into overlapping segments of 1200 characters to ensure context is preserved across pages.
3. **Vectorization:** `mxbai-embed-large` converts these text chunks into mathematical vectors.
4. **Retrieval:** When you ask a question (e.g., "Wie viel Wasser?"), the system finds the 5 most relevant segments in the PDF.
5. **Generation:** The `Gemma:2b` model receives the question + the PDF segments and writes a response based **strictly** on that context.

## ⚠️ Important Note on Deployment

This application is designed for **local use**. If you wish to deploy this to **Streamlit Cloud**, you must replace the `Ollama` components with a cloud-hosted API (like Groq or OpenAI) because Streamlit Cloud does not support local Ollama instances natively.

---
