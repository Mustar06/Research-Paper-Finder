# 🔬 Research Paper Finder

**An AI-powered research discovery agent for exploring scientific literature, comparing methodologies, and identifying research opportunities.**

Research Paper Finder transforms a high-level research question into targeted academic searches, retrieves relevant publications from seven scholarly sources, ranks papers by semantic relevance, and generates a structured literature review with methodological comparisons, mathematical formulations, computational considerations, research gaps, and a proposed implementation roadmap.

Built with Python, Streamlit, LangChain, OpenAI models, FAISS, and Pydantic.

## ✨ Features

- **Intelligent query decomposition:** Converts a research problem into structured Boolean search queries, scientific domains, and methodology keywords using an OpenAI language model.
- **Seven academic sources:** Searches arXiv, Semantic Scholar, OpenAlex, PubMed, Crossref, DBLP, and Europe PMC.
- **Paper deduplication:** Normalizes paper titles to reduce duplicate results across queries and academic databases.
- **Semantic retrieval with FAISS:** Embeds publication metadata and abstracts using OpenAI embeddings, then retrieves papers relevant to the original research problem.
- **Structured literature synthesis:** Produces a machine-validated research report containing:
  - Executive summary of the research landscape
  - Paper relevance scores from 1–10
  - Methodology classifications and core algorithmic contributions
  - Mathematical formulations and loss functions
  - Reported or inferred computational complexity considerations
  - Paper links and publication metadata
  - Unresolved literature gaps
  - A proposed technical implementation roadmap
- **Interactive Streamlit interface:** Configure the model, paper limit, and minimum relevance score through the sidebar.
- **Research analytics:** Explore publication years, relevance scores, methodology categories, and source directories using an interactive Plotly scatter plot.

## 🏗️ How It Works

The application follows a four-stage research workflow.

```text
Research Problem
      │
      ▼
1. Query Decomposition
   OpenAI + LangChain + Pydantic
      │
      ▼
2. Academic Literature Retrieval
   arXiv · Semantic Scholar · OpenAlex
   PubMed · Crossref · DBLP · Europe PMC
      │
      ▼
   Title Normalization
   and Deduplication
      │
      ▼
3. Semantic Retrieval
   OpenAI Embeddings + FAISS
      │
      ▼
4. Literature Synthesis
   Structured LLM Output
      │
      ▼
   Executive Summary
   Comparative Literature Matrix
   Research Gaps
   Proposed Technical Roadmap
```

### Stage 1: Query decomposition

The research problem is processed by an OpenAI chat model through LangChain. Pydantic structured output validation defines the expected query decomposition, including Boolean search strings, core scientific domains, and methodology keywords.

### Stage 2: Academic literature retrieval

The ingestion engine queries seven academic services and converts their results into a common paper representation containing fields such as title, authors, year, venue, citations, summary, source, and paper URL.

Titles are normalized to reduce duplicate records.

### Stage 3: Semantic retrieval

Paper records are converted into LangChain documents and embedded with OpenAI embeddings. A FAISS vector store retrieves documents semantically related to the original research question.

The current application requests the full deduplicated corpus for retrieval, subject to the number of results actually returned by the academic sources.

### Stage 4: Literature synthesis

The retrieved context is passed to the language model, which generates a structured report validated against Pydantic schemas. The Streamlit interface presents the resulting summary, paper comparison table, relevance plot, implementation roadmap, and identified literature gaps.

## 🌐 Supported Academic Sources

| Source | Primary coverage |
|---|---|
| [arXiv](https://arxiv.org/) | Physics, mathematics, computer science, and AI preprints |
| [Semantic Scholar](https://www.semanticscholar.org/) | Scientific literature, abstracts, and citation metadata |
| [OpenAlex](https://openalex.org/) | Scholarly works, authors, venues, and citation metadata |
| [PubMed](https://pubmed.ncbi.nlm.nih.gov/) | Biomedical and life sciences literature |
| [Crossref](https://www.crossref.org/) | Scholarly publication metadata and DOI records |
| [DBLP](https://dblp.org/) | Computer science publications and bibliographic records |
| [Europe PMC](https://europepmc.org/) | Biomedical and life sciences literature |

**Important:** These sources expose different fields and levels of detail. Not every result contains an abstract, citation count, or direct PDF link. Some records link to publication landing pages instead of full-text papers.

## 🧰 Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic and data processing |
| Streamlit | Interactive web interface |
| LangChain | Language-model orchestration, prompts, and document retrieval |
| OpenAI API | Query decomposition, embeddings, and literature synthesis |
| Pydantic | Structured output schemas and validation |
| FAISS | Vector indexing and semantic similarity retrieval |
| Pandas | Tabular research data |
| Plotly | Interactive literature visualization |
| Requests | Academic API requests |
| arXiv Python client | arXiv search and metadata retrieval |
| python-dotenv | Environment variable loading |

## 📁 Project Structure

```text
Research-Paper-Finder/
│
├── app.py
│   └── Streamlit interface and research workflow
│
├── src/
│   ├── agents.py
│   │   └── Query decomposition, embeddings,
│   │       retrieval, and literature synthesis
│   │
│   └── ingestion.py
│       └── Seven-source academic search engine
│
├── requirement.txt
│   └── Python dependencies
│
├── pyproject.toml
│   └── Project and build configuration
│
├── uv.lock
│   └── Dependency lockfile
│
├── .python-version
│   └── Python version configuration
│
├── .gitignore
│
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python version compatible with the project and its dependencies. The current `pyproject.toml` specifies Python 3.14 or newer.
- An OpenAI API key with access to the selected chat model and embedding model.
- Internet connectivity for OpenAI and academic API requests.

### 1. Clone the repository

```bash
git clone https://github.com/Mustar06/Research-Paper-Finder.git
cd Research-Paper-Finder
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

macOS or Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirement.txt
```

### 4. Configure your OpenAI API key

Create a `.env` file in the project root:

```dotenv
OPENAI_API_KEY=your_openai_api_key_here
```

Keep the `.env` file private and never commit your API key to GitHub.

Alternatively, enter your API key directly into the password-protected field in the Streamlit sidebar when running the application.

### 5. Launch the application

```bash
streamlit run app.py
```

Streamlit will display a local URL in your terminal. Open it in your browser to use the application.

## 🖥️ Using the Application

1. Enter your OpenAI API key in the sidebar, or configure it through `.env`.
2. Select the language model: `gpt-4o` or `gpt-4o-mini`.
3. Adjust the maximum number of papers requested per source query.
4. Set the minimum relevance score to control which evaluated papers appear in the results.
5. Describe your research problem, technical challenge, or theoretical bottleneck.
6. Click **Run Comprehensive Discovery**.
7. Review the executive summary and explore the four output tabs.

### Example research question

> Investigate efficient state-space models for real-time edge robotics, focusing on quantization, inference latency, memory consumption, and unresolved algorithmic limitations.

The system uses the problem statement to search the literature and generate a comparative research report. Results depend on the coverage of the connected academic services and the quality of their metadata.

## 📊 Outputs

### Comparative literature matrix

The interactive table presents evaluated publications with fields including title, relevance score, source directory, publication year, methodology category, core algorithm, mathematical formulation, computational considerations, and paper URL.

### Impact and relevance visualization

The Plotly scatter plot compares publication year with relevance score. Colors distinguish methodology categories, while marker symbols distinguish source directories.

### Proposed technical roadmap

The model generates an ordered set of proposed engineering steps based on the retrieved literature and the research problem.

### Literature gaps

The report identifies potential unresolved questions and bottlenecks inferred from the retrieved research context.

These outputs are AI-generated research assistance, not independently verified scientific conclusions. Mathematical equations, complexity claims, citations, and proposed research gaps should be checked against the original publications.

## 🔐 API Usage and Costs

This application makes requests to the OpenAI API for language-model inference and text embeddings. Those requests may incur charges depending on model selection, token usage, and current API pricing.

Academic search services may impose their own rate limits, access restrictions, or usage policies.

To control usage:

- Begin with a narrow research question.
- Use a lower per-source result limit for initial experiments.
- Use `gpt-4o-mini` when it meets your quality requirements.
- Avoid repeatedly running the same large search without a caching strategy.
- Monitor your OpenAI API usage and spending limits.

## ⚠️ Current Limitations

- **Metadata quality varies:** Academic databases differ in their coverage of abstracts, publication years, authors, and citation counts.
- **Not all records contain full text:** The current workflow primarily indexes metadata and available summaries or abstracts, rather than downloading and reading every full-text PDF.
- **Retrieval is corpus-dependent:** Semantic search can only retrieve records successfully ingested into the vector store.
- **Model-generated analysis needs verification:** Relevance scores, mathematical descriptions, complexity claims, and literature gaps should not be treated as ground truth.
- **Search reliability varies:** Individual source failures can result in incomplete results. The current ingestion implementation catches several exceptions without reporting detailed diagnostics.
- **Rate limits apply:** The application does not guarantee unrestricted access to third-party academic services.
- **No persistent research index:** FAISS is constructed in memory for the current run; the application does not currently implement a persistent vector database or cross-session research cache.
- **Research completeness is not guaranteed:** A generated review is not a substitute for a systematic literature review with a documented search protocol and manual screening.

## 🛣️ Potential Improvements

The project could be extended with:

- Persistent vector storage and cached search results
- Source-specific error reporting, retries, and rate-limit handling
- Citation verification and DOI normalization
- PDF ingestion and full-text analysis
- Configurable publication date and venue filters
- More robust deduplication using DOI and bibliographic identifiers
- Exportable reports in Markdown, CSV, or PDF
- Evaluation benchmarks for retrieval quality and factual accuracy
- Source provenance for each claim in the generated synthesis
- Reproducible search logs and research-session history

## 🤝 Contributing

Contributions, bug reports, and feature suggestions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Make your changes and test them locally.
4. Submit a pull request describing the changes and their expected impact.

## 📄 License

No license is currently specified in this README. Add an appropriate license file before distributing the project under an open-source license.

## 👨‍💻 Author

**Mustafa Hamid Talukdar**

GitHub: [@Mustar06](https://github.com/Mustar06)

Project: [Research Paper Finder](https://github.com/Mustar06/Research-Paper-Finder)

---

*Research Paper Finder is an experimental AI-assisted literature discovery tool intended to help researchers explore scientific publications and investigate promising research directions.*
