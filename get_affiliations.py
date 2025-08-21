import requests
import csv
import time
import sys
from urllib.parse import urlparse

def get_doi_from_url(url):
    """
    Extract DOI from ACM DL URL or direct DOI URL.
    """
    try:
        parsed = urlparse(url)
        
        if parsed.netloc == "doi.org":
            return parsed.path.lstrip("/")
        
    except Exception:
        pass
    return None

def fetch_metadata(doi):
    """Fetch JSON metadata from CrossRef for a DOI."""
    url = f"https://api.crossref.org/works/{doi}"
    headers = {"Accept": "application/json"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        return r.json()["message"]
    except requests.RequestException as e:
        print(f"Error fetching {doi}: {e}")
        return None

def extract_authors(metadata):
    """Extract author names and affiliations from CrossRef metadata."""
    authors_data = []
    if "author" in metadata:
        for author in metadata["author"]:
            name_parts = []
            if "given" in author:
                name_parts.append(author["given"])
            if "family" in author:
                name_parts.append(author["family"])
            full_name = " ".join(name_parts)

            affiliation_list = []
            if "affiliation" in author:
                affiliation_list = [aff["name"] for aff in author["affiliation"] if "name" in aff]

            authors_data.append({
                "name": full_name,
                "affiliations": "; ".join(affiliation_list) if affiliation_list else ""
            })
    return authors_data

def main():
    if len(sys.argv) != 3:
        print("Usage: python fetch_acm_affiliations.py <input_csv_path> <output_csv_path>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    rows_out = []

    with open(input_file, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            acm_url = row["url"]
            doi = get_doi_from_url(acm_url)
            if not doi:
                print(f"Could not extract DOI from: {acm_url}")
                continue

            print(f"Fetching metadata for DOI: {doi}")
            metadata = fetch_metadata(doi)
            if not metadata:
                continue

            authors = extract_authors(metadata)

            for author in authors:
                rows_out.append({
                    "reviewer": row["reviewer"],
                    "relevant": row["relevant"],
                    "title": row["title"],
                    "original_authors": row["authors"],
                    "url": row["url"],
                    "extracted_author": author["name"],
                    "affiliations": author["affiliations"]
                })

    # Write results
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["reviewer", "relevant", "title", "original_authors", "url", "extracted_author", "affiliations"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows_out)

    print(f"Done! Saved {len(rows_out)} author entries to {output_file}")

if __name__ == "__main__":
    main()
