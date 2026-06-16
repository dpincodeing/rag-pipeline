<div align="center">

# 📄 PDF RAG Pipeline

**A local, privacy-first Retrieval-Augmented Generation system — ask questions about any PDF, powered entirely by open-source models.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-🦜-1C3C3C?style=for-the-badge)](https://www.langchain.com/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_Store-FF6B35?style=for-the-badge)](https://www.trychroma.com/)
[![Ollama](https://img.shields.io/badge/Ollama-llama3.2-black?style=for-the-badge)](https://ollama.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

</div>

---

## ✨ Features

- 🔒 **100% Local** — no API keys, no data leaves your machine
- 📚 **PDF Ingestion** — load and chunk any PDF document automatically
- 🧠 **Semantic Search** — HuggingFace embeddings (`all-MiniLM-L6-v2`) power fast, accurate retrieval
- 💬 **LLM Answering** — Ollama runs `llama3.2` locally for context-aware responses
- 🗃️ **Query Logging** — every Q&A is persisted to SQLite with response times
- 📊 **Usage Stats** — view query history, average latency, and total request counts

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        INGESTION PIPELINE                       │
│                                                                 │
│  document.pdf  ──►  PyPDFLoader  ──►  RecursiveTextSplitter     │
│                                           │                     │
│                                    (chunk_size=500,             │
│                                     chunk_overlap=50)           │
│                                           │                     │
│                                           ▼                     │
│                                  HuggingFace Embeddings         │
│                                  (all-MiniLM-L6-v2)            │
│                                           │                     │
│                                           ▼                     │
│                                     ChromaDB  💾                │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                         QUERY PIPELINE                          │
│                                                                 │
│  User Question  ──►  Similarity Search (k=1)                   │
│                              │                                  │
│                              ▼                                  │
│                       Retrieved Chunks                          │
│                              │                                  │
│                              ▼                                  │
│                    Prompt: Context + Question                   │
│                              │                                  │
│                              ▼                                  │
│                      Ollama (llama3.2)  🦙                      │
│                              │                                  │
│                    ┌─────────┴─────────┐                        │
│                    ▼                   ▼                        │
│                 Answer          SQLite Log 📋                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) installed and running

### 1. Clone the repository

```bash
git clone https://github.com/dpincodeing/rag-pipeline.git
cd rag-pipeline
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Pull the LLM model

```bash
ollama pull llama3.2
```

### 4. Add your PDF

Place your PDF file in the project root and rename it (or update the path in `ingest.py`):

```bash
cp /path/to/your/document.pdf ./document.pdf
```

### 5. Ingest the PDF

```bash
python ingest.py
```

> This chunks your PDF and stores vector embeddings in `./chroma_db/`.

### 6. Ask a question

```python
# Edit ask.py and set your question, then run:
python ask.py
```

---

## 📁 Project Structure

```
pdf-rag/
├── ingest.py          # Load, chunk, embed, and store PDF into ChromaDB
├── ask.py             # Query the vector store and get LLM answers
├── db.py              # SQLite logging — init schema and log queries
├── stats.py           # View query history, avg latency, total count
├── requirements.txt   # Python dependencies
├── chroma_db/         # Persisted vector store (auto-generated)
├── rag_logs.db        # SQLite query log (auto-generated)
└── document.pdf       # Your source PDF (not tracked in git)
```

---

## 📂 File Reference

| File | Purpose |
|------|---------|
| [`ingest.py`](ingest.py) | Loads PDF → splits into chunks → embeds with HuggingFace → saves to ChromaDB |
| [`ask.py`](ask.py) | Embeds the query → retrieves relevant chunks → sends to Ollama → logs result |
| [`db.py`](db.py) | SQLite helpers: `init_db()` creates schema, `log_query()` persists each Q&A |
| [`stats.py`](stats.py) | Prints recent queries, average response time, and total query count |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Document Loading** | [LangChain PyPDFLoader](https://python.langchain.com/docs/integrations/document_loaders/pypdf/) |
| **Text Splitting** | LangChain `RecursiveCharacterTextSplitter` |
| **Embeddings** | [HuggingFace `all-MiniLM-L6-v2`](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) |
| **Vector Store** | [ChromaDB](https://www.trychroma.com/) |
| **LLM** | [Ollama](https://ollama.com/) with `llama3.2` |
| **Logging** | SQLite via Python `sqlite3` |
| **Orchestration** | [LangChain](https://www.langchain.com/) |

---

## 📊 Monitoring Queries

Run `stats.py` to view analytics from the SQLite log:

```bash
python stats.py
```

**Example output:**
```
--- Recent queries ---
('What is the main topic?', 342, '2024-01-15 10:23:45')
('Summarize chapter 2', 289, '2024-01-15 10:24:12')

--- Average response time ---
(315.5,)

--- Total queries ---
(2,)
```

---

## ⚙️ Configuration

You can tweak these parameters to tune performance:

| Parameter | Location | Default | Description |
|-----------|----------|---------|-------------|
| `chunk_size` | `ingest.py` | `500` | Characters per chunk |
| `chunk_overlap` | `ingest.py` | `50` | Overlap between chunks |
| `k` (retrieval) | `ask.py` | `1` | Number of chunks retrieved |
| `model` | `ask.py` | `llama3.2` | Ollama model to use |
| `embedding model` | `ingest.py` / `ask.py` | `all-MiniLM-L6-v2` | HuggingFace embedding model |

---

## 🔮 Roadmap

- [ ] CLI interface with `argparse` for interactive Q&A
- [ ] Support for multiple PDFs / document collections
- [ ] Streaming LLM responses
- [ ] Web UI (Gradio or Streamlit)
- [ ] Re-ranking retrieved chunks
- [ ] Configurable via `.env` or `config.yaml`

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <sub>Built with ❤️ using LangChain, ChromaDB, and Ollama</sub>
</div>
