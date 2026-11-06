from typing import List, Dict, Any
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate

class QueryDecomposition(BaseModel):
    boolean_queries: List[str] = Field(description="3-4 distinct Boolean search strings.")
    core_domains: List[str] = Field(description="Primary scientific disciplines involved.")
    methodology_keywords: List[str] = Field(description="Algorithmic or hardware keywords.")

class IndividualPaperEvaluation(BaseModel):
    title: str = Field(description="Exact paper title")
    authors: List[str] = Field(description="Authors list")
    year: int = Field(description="Publication year")
    source_directory: str = Field(description="Origin directory")
    relevance_score: int = Field(description="Relevance score from 1 to 10")
    methodology_category: str = Field(description="Methodological paradigm classification")
    core_algorithm: str = Field(description="Explanation of key algorithmic innovation")
    mathematical_formulation: str = Field(description="Primary equations or loss functions used")
    compute_complexity: str = Field(description="Memory or latency bounds noted")
    pdf_url: str = Field(description="Direct URL to paper or PDF")

class LiteratureSynthesisReport(BaseModel):
    executive_summary: str = Field(description="State-of-the-art overview across literature.")
    taxonomy_breakdown: str = Field(description="Categorical breakdown of methods and trade-offs.")
    identified_literature_gaps: List[str] = Field(description="Unresolved literature bottlenecks.")
    proposed_roadmap: List[str] = Field(description="Ordered, actionable architectural steps.")
    paper_evaluations: List[IndividualPaperEvaluation] = Field(description="Paper evaluations list")

class ResearchAgentPipeline:
    def __init__(self, api_key: str, model_name: str = "gpt-4o"):
        self.llm = ChatOpenAI(model=model_name, api_key=api_key, temperature=0.1)
        self.embeddings = OpenAIEmbeddings(openai_api_key=api_key)

    def decompose(self, problem: str) -> QueryDecomposition:
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a Senior AI Research Strategist. Break down problem statements into Boolean search queries and domain tags."),
            ("user", "Problem Statement:\n{problem}")
        ])
        chain = prompt | self.llm.with_structured_output(QueryDecomposition)
        return chain.invoke({"problem": problem})

    def build_rag_context(self, papers: List[Dict[str, Any]], problem: str, top_k: int = 6) -> str:
        docs = []
        for p in papers:
            content = (
                f"Title: {p['title']}\n"
                f"Authors: {', '.join(p['authors'])}\n"
                f"Year: {p['year']} | Source Directory: {p['source']} | Venue: {p['venue']}\n"
                f"Citations: {p['citations']}\n"
                f"Abstract/Summary: {p['summary']}"
            )
            docs.append(Document(page_content=content, metadata={"title": p["title"], "pdf_url": p["pdf_url"]}))
        
        vectorstore = FAISS.from_documents(docs, self.embeddings)
        retriever = vectorstore.as_retriever(search_kwargs={"k": min(top_k, len(docs))})
        matched_docs = retriever.invoke(problem)
        return "\n\n---\n\n".join([d.page_content for d in matched_docs])

    def synthesize(self, problem: str, rag_context: str) -> LiteratureSynthesisReport:
        prompt = ChatPromptTemplate.from_messages([
            ("system", 
             "You are a Senior Principal AI Scientist. Conduct a mathematically precise literature analysis "
             "using the provided RAG context across research directories. Extract mathematical formulas, "
             "compute complexity bounds, literature gaps, and a step-by-step implementation roadmap."),
            ("user", "Problem Statement:\n{problem}\n\nRAG Context:\n{rag_context}")
        ])
        chain = prompt | self.llm.with_structured_output(LiteratureSynthesisReport)
        return chain.invoke({"problem": problem, "rag_context": rag_context})