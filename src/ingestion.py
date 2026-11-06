import re
import urllib.parse
import requests
from typing import List, Dict, Any
import arxiv

class UniversalPaperIngestionEngine:
    
    @staticmethod
    def search_arxiv(query: str, max_results: int = 3) -> List[Dict[str, Any]]:
        results = []
        try:
            client = arxiv.Client()
            search = arxiv.Search(query=query, max_results=max_results, sort_by=arxiv.SortCriterion.Relevance)
            for r in client.results(search):
                results.append({
                    "id": r.entry_id,
                    "title": r.title.replace("\n", " ").strip(),
                    "authors": [a.name for a in r.authors],
                    "year": r.published.year,
                    "venue": "arXiv Pre-print",
                    "citations": 0,
                    "summary": r.summary.replace("\n", " ").strip(),
                    "pdf_url": r.pdf_url,
                    "source": "arXiv"
                })
        except Exception:
            pass
        return results

    @staticmethod
    def search_semantic_scholar(query: str, max_results: int = 3) -> List[Dict[str, Any]]:
        results = []
        url = "https://api.semanticscholar.org/graph/v1/paper/search"
        params = {"query": query, "limit": max_results, "fields": "title,authors,year,venue,citationCount,abstract,openAccessPdf"}
        try:
            res = requests.get(url, params=params, timeout=8)
            if res.status_code == 200:
                for item in res.json().get("data", []):
                    pdf_info = item.get("openAccessPdf") or {}
                    results.append({
                        "id": item.get("paperId", item.get("title")),
                        "title": item.get("title", "Untitled").strip(),
                        "authors": [a["name"] for a in item.get("authors", [])],
                        "year": item.get("year") or 2024,
                        "venue": item.get("venue") or "Peer-Reviewed / S2",
                        "citations": item.get("citationCount") or 0,
                        "summary": item.get("abstract") or "No abstract provided.",
                        "pdf_url": pdf_info.get("url", f"https://www.semanticscholar.org/paper/{item.get('paperId')}"),
                        "source": "Semantic Scholar"
                    })
        except Exception:
            pass
        return results

    @staticmethod
    def search_openalex(query: str, max_results: int = 3) -> List[Dict[str, Any]]:
        results = []
        url = f"https://api.openalex.org/works?search={urllib.parse.quote(query)}&per_page={max_results}"
        try:
            res = requests.get(url, timeout=8, headers={"User-Agent": "ResearchAgent/1.0"})
            if res.status_code == 200:
                for item in res.json().get("results", []):
                    abstract_dict = item.get("abstract_inverted_index")
                    abstract_text = "No abstract available."
                    if abstract_dict:
                        word_list = []
                        for word, positions in abstract_dict.items():
                            for pos in positions:
                                word_list.append((pos, word))
                        word_list.sort()
                        abstract_text = " ".join([w[1] for w in word_list])

                    authorships = item.get("authorships", [])
                    authors = [a.get("author", {}).get("display_name", "") for a in authorships if a.get("author")]
                    primary_loc = item.get("primary_location") or {}

                    results.append({
                        "id": item.get("id"),
                        "title": item.get("title", "Untitled").strip(),
                        "authors": authors[:5],
                        "year": item.get("publication_year") or 2024,
                        "venue": primary_loc.get("source", {}).get("display_name") or "OpenAlex Index",
                        "citations": item.get("cited_by_count") or 0,
                        "summary": abstract_text,
                        "pdf_url": primary_loc.get("pdf_url") or item.get("doi") or item.get("id"),
                        "source": "OpenAlex"
                    })
        except Exception:
            pass
        return results

    @staticmethod
    def search_pubmed(query: str, max_results: int = 3) -> List[Dict[str, Any]]:
        results = []
        try:
            search_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={urllib.parse.quote(query)}&retmode=json&retmax={max_results}"
            s_res = requests.get(search_url, timeout=8).json()
            id_list = s_res.get("esearchresult", {}).get("idlist", [])

            if id_list:
                ids_str = ",".join(id_list)
                summary_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={ids_str}&retmode=json"
                sum_res = requests.get(summary_url, timeout=8).json().get("result", {})

                for pmid in id_list:
                    pdata = sum_res.get(pmid, {})
                    if pdata:
                        authors = [a.get("name", "") for a in pdata.get("authors", [])]
                        pub_date = pdata.get("pubdate", "2024")
                        year = int(pub_date.split()[0]) if pub_date.split()[0].isdigit() else 2024
                        results.append({
                            "id": f"PMID:{pmid}",
                            "title": pdata.get("title", "Untitled").strip(),
                            "authors": authors[:5],
                            "year": year,
                            "venue": pdata.get("source", "PubMed Central"),
                            "citations": 0,
                            "summary": f"Indexed under PMID {pmid} in NCBI PubMed.",
                            "pdf_url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                            "source": "PubMed"
                        })
        except Exception:
            pass
        return results

    @staticmethod
    def search_crossref(query: str, max_results: int = 3) -> List[Dict[str, Any]]:
        results = []
        url = f"https://api.crossref.org/works?query={urllib.parse.quote(query)}&rows={max_results}"
        try:
            res = requests.get(url, timeout=8, headers={"User-Agent": "ResearchAgent/1.0"})
            if res.status_code == 200:
                for item in res.json().get("message", {}).get("items", []):
                    title_list = item.get("title", [])
                    title = title_list[0] if title_list else "Untitled"
                    authors = [f"{a.get('given', '')} {a.get('family', '')}".strip() for a in item.get("author", [])]
                    published = item.get("published-print") or item.get("published-online") or {}
                    year_parts = published.get("date-parts", [[2024]])[0]
                    year = year_parts[0] if len(year_parts) > 0 else 2024

                    results.append({
                        "id": item.get("DOI", title),
                        "title": title.strip(),
                        "authors": authors[:5],
                        "year": year,
                        "venue": item.get("container-title", ["Crossref Journal"])[0] if item.get("container-title") else "Crossref",
                        "citations": item.get("is-referenced-by-count") or 0,
                        "summary": item.get("abstract") or "Metadata record indexed via Crossref.",
                        "pdf_url": item.get("URL", f"https://doi.org/{item.get('DOI')}"),
                        "source": "Crossref"
                    })
        except Exception:
            pass
        return results

    @staticmethod
    def search_dblp(query: str, max_results: int = 3) -> List[Dict[str, Any]]:
        results = []
        url = f"https://dblp.org/search/pub/api?q={urllib.parse.quote(query)}&format=json&h={max_results}"
        try:
            res = requests.get(url, timeout=8)
            if res.status_code == 200:
                hits = res.json().get("result", {}).get("hits", {}).get("hit", [])
                for hit in hits:
                    info = hit.get("info", {})
                    authors_data = info.get("authors", {}).get("author", [])
                    if isinstance(authors_data, dict):
                        authors_data = [authors_data]
                    authors = [a.get("text", "") for a in authors_data]

                    results.append({
                        "id": info.get("key", info.get("title")),
                        "title": info.get("title", "Untitled").strip("."),
                        "authors": authors[:5],
                        "year": int(info.get("year", 2024)),
                        "venue": info.get("venue", "DBLP Index"),
                        "citations": 0,
                        "summary": f"Indexed publication in DBLP Computer Science Bibliography. Type: {info.get('type', 'Publication')}.",
                        "pdf_url": info.get("ee", f"https://dblp.org/rec/{info.get('key')}"),
                        "source": "DBLP"
                    })
        except Exception:
            pass
        return results

    @staticmethod
    def search_europe_pmc(query: str, max_results: int = 3) -> List[Dict[str, Any]]:
        results = []
        url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={urllib.parse.quote(query)}&format=json&pageSize={max_results}"
        try:
            res = requests.get(url, timeout=8)
            if res.status_code == 200:
                results_list = res.json().get("resultList", {}).get("result", [])
                for item in results_list:
                    results.append({
                        "id": item.get("id"),
                        "title": item.get("title", "Untitled").strip("."),
                        "authors": [item.get("authorString", "Unknown")],
                        "year": int(item.get("pubYear", 2024)),
                        "venue": item.get("journalTitle", "Europe PMC"),
                        "citations": item.get("citedByCount") or 0,
                        "summary": item.get("abstractText") or "No abstract provided in Europe PMC repository.",
                        "pdf_url": f"https://europepmc.org/article/{item.get('source', 'MED')}/{item.get('id')}",
                        "source": "Europe PMC"
                    })
        except Exception:
            pass
        return results

    @classmethod
    def fetch_all_directories(cls, query: str, max_per_source: int = 2) -> List[Dict[str, Any]]:
        all_hits = (
            cls.search_arxiv(query, max_per_source) +
            cls.search_semantic_scholar(query, max_per_source) +
            cls.search_openalex(query, max_per_source) +
            cls.search_pubmed(query, max_per_source) +
            cls.search_crossref(query, max_per_source) +
            cls.search_dblp(query, max_per_source) +
            cls.search_europe_pmc(query, max_per_source)
        )

        deduped = []
        seen_titles = set()
        for p in all_hits:
            clean_title = re.sub(r'\W+', '', p["title"].lower())
            if clean_title and clean_title not in seen_titles:
                seen_titles.add(clean_title)
                deduped.append(p)

        return deduped