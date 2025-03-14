import requests
import csv
import re
from typing import List, Dict

PUBMED_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_SUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

def fetch_paper_ids(query: str) -> List[str]:
    params = {"db": "pubmed", "term": query, "retmode": "json", "retmax": 10}
    response = requests.get(PUBMED_API_URL, params=params)
    response.raise_for_status()
    return response.json().get("esearchresult", {}).get("idlist", [])

def fetch_paper_details(paper_ids: List[str]) -> List[Dict]:
    if not paper_ids:
        return []

    params = {"db": "pubmed", "id": ",".join(paper_ids), "retmode": "json"}
    response = requests.get(PUBMED_SUMMARY_URL, params=params)
    response.raise_for_status()
    
    data = response.json()
    results = []

    for paper_id in paper_ids:
        paper = data.get("result", {}).get(paper_id, {})
        authors = paper.get("authors", [])
        non_academic_authors = [
            a['name'] for a in authors if not re.search(r"(university|lab|college)", a.get("affiliation", "").lower())
        ]
        company_affiliations = [
            a.get("affiliation", "") for a in authors if re.search(r"(pharma|biotech|inc|ltd|gmbh|corp)", a.get("affiliation", "").lower())
        ]
        
        results.append({
            "PubmedID": paper_id,
            "Title": paper.get("title", "N/A"),
            "Publication Date": paper.get("pubdate", "N/A"),
            "Non-academic Authors": ", ".join(non_academic_authors),
            "Company Affiliations": ", ".join(company_affiliations),
            "Corresponding Author Email": paper.get("contactemail", "N/A")
        })
    
    return results

def save_to_csv(papers: List[Dict], filename: str):
    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=papers[0].keys())
        writer.writeheader()
        writer.writerows(papers)
