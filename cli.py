import argparse
from research_papers.fetch_papers import fetch_paper_ids, fetch_paper_details, save_to_csv

def main():
    parser = argparse.ArgumentParser(description="Fetch PubMed research papers based on a query.")
    parser.add_argument("query", type=str, help="Search query for PubMed")
    parser.add_argument("-f", "--file", type=str, help="Filename to save results")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    
    args = parser.parse_args()
    
    if args.debug:
        print(f"Fetching papers for query: {args.query}")

    paper_ids = fetch_paper_ids(args.query)
    if args.debug:
        print(f"Found paper IDs: {paper_ids}")

    papers = fetch_paper_details(paper_ids)

    if args.file:
        save_to_csv(papers, args.file)
        print(f"Results saved to {args.file}")
    else:
        for paper in papers:
            print(paper)

if __name__ == "__main__":
    main()
