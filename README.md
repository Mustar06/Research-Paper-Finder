# 🔬 Research-Paper-Finder

An **Autonomous Multi-Directory AI Literature Discovery Agent** built with **LangChain**, **Streamlit**, **FAISS Vector RAG**, and **OpenAI GPT-4o**. 

This platform automates academic literature reviews by deconstructing complex engineering bottlenecks into targeted search queries, ingesting papers concurrently across **7 global academic directories**, indexing abstract embeddings inside an in-memory vector store, and synthesizing structured comparative literature matrices alongside actionable implementation roadmaps.

---

## 🌟 Key Features

* **Automated Query Decomposition**: Uses GPT-4o with Pydantic structured output validation to deconstruct high-level problem statements into 3–5 Boolean search strings, domain tags, and algorithmic keywords.
* **Universal 7-Directory Ingestion**: Concurrently queries **arXiv**, **Semantic Scholar**, **OpenAlex**, **PubMed**, **Crossref**, **DBLP**, and **Europe PMC** without artificial throttling.
* **Title Normalization & Deduplication**: Cleans non-alphanumeric noise and normalizes titles to prevent cross-platform duplicated paper entries.
* **FAISS Vector Retrieval-Augmented Generation (RAG)**: Converts abstract text into dense mathematical vector representations using `OpenAIEmbeddings` and retrieves top semantic matches via similarity search.
* **Multi-Dimensional Literature Matrix**: Synthesizes structured paper analyses including:
  * Relevance scoring (1–10)
  * Methodological paradigm classification
  * Core algorithmic innovations
  * Explicit mathematical formulations & loss functions
  * Computational complexity bounds (latency, memory limits)
  * Direct PDF / DOI landing links
* **Interactive Streamlit UI & Analytics**:
  * **Interactive Matrix Table**: View and filter structured paper data.
  * **Plotly Spectrum Plot**: Analyze publication timelines versus relevance scores grouped by source directory.
  * **Architectural Roadmap**: Sequential, actionable engineering steps derived from literature gaps.
  * **Literature Gaps**: Identifies open theoretical bottlenecks in the ingested corpus.

---

## 🌐 Supported Academic Directories

| Directory Source | Domain Focus / Coverage | Access Protocol |
| :--- | :--- | :--- |
| **arXiv** | Physics, Computer Science, Quantitative Finance, Mathematics, AI | REST API (`arxiv` Client) |
| **Semantic Scholar** | General Science, Computer Science, Biomedicine | Graph API |
| **OpenAlex** | Global Scholarly Web (Over 250M works) | REST API |
| **PubMed** | Biomedical and Life Sciences Literature | NCBI E-Utilities API |
| **Crossref** | Academic Journals, Conference Proceedings, DOIs | REST API |
| **DBLP** | Computer Science Bibliography | REST API |
| **Europe PMC** | Life Sciences, Biological Research, PubMed Central | REST API |

---

## 🏗️ Architecture & Agentic Workflow

```text
[ User Problem Statement ]
          │
          ▼
┌─────────────────────────────────────────────────────────┐
│ Step 1: Query Decomposition Agent (LangChain + GPT-4o)  │
│  └─ Outputs Boolean Queries, Domains & Methodology Keys  │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ Step 2: Universal 7-Directory Ingestion Engine         │
│  ├─ Parallel Queries: arXiv, Semantic Scholar, OpenAlex,│
│  │   PubMed, Crossref, DBLP, Europe PMC                 │
│  └─ Dynamic Alphanumeric Title Deduplication            │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ Step 3: FAISS Vector RAG Engine                        │
│  ├─ Document Chunk
