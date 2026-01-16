# 🛡️ Langchain Chatbot Guide for Catastrophe Preparation

StreamlitUI: https://langchain-chatbot-guide-for-catastrophe-preparation.streamlit.app/
Repo: https://github.com/iceyisaak/langchain-chatbot-guide-for-catastrophe-preparation

---

An AI-powered emergency preparedness assistant based on official guidance from the **BBK (Bundesamt für Bevölkerungsschutz und Katastrophenhilfe)**.

This version is designed for high performance and easy deployment using **Groq** for ultra-fast LLM inference and **HuggingFace** for efficient text embeddings.

## 🚀 Features

* **Cloud-Ready:** Fully compatible with Streamlit Cloud—no local Ollama instance required.
* **Blazing Fast:** Powered by Groq's LPU™ Inference Engine for near-instant responses.
* **Smart Retrieval:** Uses `all-MiniLM-L6-v2` embeddings to match user queries with the most relevant sections of the BBK guide.
* **Contextual Accuracy:** Answers are strictly grounded in the provided PDF documentation to ensure safety and reliability.

## 🛠️ Tech Stack

* **LLM:** `llama-3.1-8b-instant` (via Groq)
* **Embeddings:** `all-MiniLM-L6-v2` (via HuggingFace)
* **Orchestration:** LangChain
* **Vector Store:** FAISS
* **Interface:** Streamlit

## ⚙️ Setup & Installation

### 1. Get Your API Keys

To run this app, you will need:

* **Groq API Key:** Get it for free at [console.groq.com](https://console.groq.com/).
* **HuggingFace Token:** Create one at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).

### 2. Local Installation

```bash
# Clone the repository
git clone https://github.com/iceyisaak/langchain-chatbot-guide-for-catastrophe-preparation.git
cd langchain-chatbot-guide-for-catastrophe-preparation

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py

```

### 3. Usage

1. Enter your **Groq API Key** and **HuggingFace Token** in the sidebar.
2. The app will automatically process any PDFs located in the `./document` folder.
3. Ask questions like *"Wie viel Wasser sollte ich pro Person lagern?"* or *"Was gehört in ein Notgepäck?"*

## 📁 Project Structure

* `app.py`: Main Streamlit application logic.
* `document/`: Directory where official BBK PDFs are stored.
* `requirements.txt`: Necessary Python packages (including `langchain-groq` and `langchain-huggingface`).

## 🤖 How It Works

1. **Document Ingestion:** The `PyPDFDirectoryLoader` reads all documents in the `./document` folder.
2. **Recursive Chunking:** Text is split into 1200-character chunks with a 600-character overlap to ensure no data is lost between "splits."
3. **Vector Store:** HuggingFace embeddings transform text into vectors stored in a FAISS index.
4. **RAG Chain:** When a user asks a question, the system retrieves the top 5 relevant text chunks and passes them to Llama 3.1 on Groq to generate a precise answer in German.

## ⚠️ Safety Disclaimer

This tool provides information based on the BBK guide. In an actual emergency, always follow instructions from local authorities and official emergency broadcasts.

---