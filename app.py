import os
import re
import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv

from src.agents import ResearchAgentPipeline
from src.ingestion import UniversalPaperIngestionEngine

load_dotenv()

st.set_page_config(page_title="Autonomous Research Agent", page_icon="🔬", layout="wide")
st.title("🔬 Autonomous Multi-Directory Research Discovery Agent")
st.caption("Ingests across arXiv, Semantic Scholar, OpenAlex, PubMed, Crossref, DBLP, and Europe PMC using FAISS Vector RAG")

with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY", ""))
    model_name = st.selectbox("LLM Core Engine", ["gpt-4o", "gpt-4o-mini"], index=0)
    max_per_source = st.slider("Max Papers per Source Query", min_value=5, max_value=50, value=20)
    min_relevance = st.slider("Min Relevance Threshold (1-10)", min_value=1, max_value=10, value=1)

problem_input = st.text_area(
    "Describe your research problem statement or theoretical bottleneck:",
    placeholder="e.g., Designing sub-milliwatt physical AI state-space models for ultra-low latency real-time edge robotics using quantized neural networks.",
    height=120
)

if st.button("🚀 Run Comprehensive Discovery", type="primary"):
    if not api_key:
        st.error("Please enter your OpenAI API key.")
        st.stop()
    if not problem_input.strip():
        st.warning("Please enter a problem statement.")
        st.stop()

    pipeline = ResearchAgentPipeline(api_key=api_key, model_name=model_name)

    with st.status("Executing Research Discovery Flow...", expanded=True) as status:
        st.write("🧩 **Step 1:** Deconstructing problem statement into Boolean queries...")
        decomp = pipeline.decompose(problem_input)
        st.write(f"Generated Queries (`{len(decomp.boolean_queries)}`): `{decomp.boolean_queries}`")

        st.write("🌐 **Step 2:** Querying all 7 global research directories concurrently...")
        raw_corpus = []
        seen = set()
        
        # Iterate over ALL generated Boolean queries
        for q in decomp.boolean_queries:
            hits = UniversalPaperIngestionEngine.fetch_all_directories(q, max_per_source=max_per_source)
            for item in hits:
                clean_t = re.sub(r'\W+', '', item["title"].lower())
                if clean_t not in seen:
                    seen.add(clean_t)
                    raw_corpus.append(item)

        st.write(f"Ingested & deduplicated **{len(raw_corpus)} unique papers** across all sources.")

        if not raw_corpus:
            status.update(label="No papers found.", state="error")
            st.error("Failed to retrieve papers. Try broadening the problem description.")
            st.stop()

        st.write("📦 **Step 3:** Indexing all abstracts into FAISS Vector RAG...")
        rag_context = pipeline.build_rag_context(raw_corpus, problem_input, top_k=len(raw_corpus))

        st.write("🧬 **Step 4:** Evaluating full paper set & synthesizing literature matrix...")
        report = pipeline.synthesize(problem_input, rag_context)

        status.update(label=f"Complete! Analyzed {len(report.paper_evaluations)} Papers.", state="complete", expanded=False)

    st.subheader("📌 Executive Summary")
    st.info(report.executive_summary)

    # Filter by Relevance Threshold
    filtered_evals = [p for p in report.paper_evaluations if p.relevance_score >= min_relevance]

    tab_matrix, tab_viz, tab_roadmap, tab_gaps = st.tabs([
        f"📋 Comparative Matrix ({len(filtered_evals)})", 
        "📈 Impact & Relevance Plot", 
        "🗺️ Architectural Roadmap", 
        "⚠️ Literature Gaps"
    ])

    with tab_matrix:
        st.subheader("Structured Paper Comparison")
        if filtered_evals:
            records = [{
                "Title": p.title,
                "Relevance": f"{p.relevance_score}/10",
                "Directory": p.source_directory,
                "Year": p.year,
                "Category": p.methodology_category,
                "Core Algorithm": p.core_algorithm,
                "Math Formulation": p.mathematical_formulation,
                "Compute Bounds": p.compute_complexity,
                "PDF Link": p.pdf_url
            } for p in filtered_evals]
            st.dataframe(pd.DataFrame(records), use_container_width=True)
        else:
            st.warning("No papers match the selected minimum relevance score.")

    with tab_viz:
        st.subheader("Literature Spectrum: Relevance vs Timeline")
        if filtered_evals:
            viz_df = pd.DataFrame([{
                "Title": p.title,
                "Year": p.year,
                "Relevance": p.relevance_score,
                "Category": p.methodology_category,
                "Directory": p.source_directory
            } for p in filtered_evals])
            fig = px.scatter(
                viz_df, 
                x="Year", 
                y="Relevance", 
                color="Category", 
                symbol="Directory",
                hover_name="Title",
                title="Cross-Directory Papers Spectrum"
            )
            st.plotly_chart(fig, use_container_width=True)

    with tab_roadmap:
        st.subheader("🗺️ Proposed Technical Roadmap")
        for idx, step in enumerate(report.proposed_roadmap, 1):
            st.markdown(f"**{idx}.** {step}")

    with tab_gaps:
        st.subheader("⚠️ Unresolved Literature Gaps")
        for gap in report.identified_literature_gaps:
            st.markdown(f"- {gap}")