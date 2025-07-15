import re
import csv
import sys
import os

def parse_bibtex_file(bib_file_path, output_csv_path):
    """
    Parse a BibTeX file and extract title, authors, and URL to a CSV file.
    """
    
    # Create the results/bib directory if it doesn't exist
    output_dir = os.path.dirname(output_csv_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    with open(bib_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Split the content into individual entries
    entries = re.split(r'@\w+\{[^,]+,', content)[1:]  # Skip the first empty split
    
    papers = []
    
    for entry in entries:
        if not entry.strip():
            continue
            
        paper_data = {}
        
        # Extract title
        title_match = re.search(r'title\s*=\s*\{([^}]+)\}', entry, re.IGNORECASE | re.DOTALL)
        if title_match:
            # Clean up the title (remove extra whitespace and newlines)
            paper_data['title'] = ' '.join(title_match.group(1).strip().split())
        else:
            paper_data['title'] = ''
        
        # Extract authors
        author_match = re.search(r'author\s*=\s*\{([^}]+)\}', entry, re.IGNORECASE | re.DOTALL)
        if author_match:
            # Clean up authors (remove extra whitespace and newlines)
            authors = ' '.join(author_match.group(1).strip().split())
            # Replace " and " with ", " for better CSV formatting
            authors = re.sub(r'\s+and\s+', ', ', authors)
            paper_data['authors'] = authors
        else:
            paper_data['authors'] = ''
        
        # Extract URL
        url_match = re.search(r'url\s*=\s*\{([^}]+)\}', entry, re.IGNORECASE)
        if url_match:
            paper_data['url'] = url_match.group(1).strip()
        else:
            paper_data['url'] = ''
        
        # Extract Abstract
        abs_match = re.search(r'abstract\s*=\s*\{([^}]+)\}', entry, re.IGNORECASE)
        if abs_match:
            paper_data['abstract'] = abs_match.group(1).strip()
        else:
            paper_data['abstract'] = ''
        
        # Only add papers that have at least a title
        if paper_data['title']:
            papers.append(paper_data)
    
    # Write to CSV
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'authors', 'url', 'abstract']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for paper in papers:
            writer.writerow(paper)
    
    print(f"Successfully parsed {len(papers)} papers from {bib_file_path}")
    print(f"Results saved to {output_csv_path}")

def extract_titles_from_bib(bib_file_path):
    """
    Extract just the titles from a BibTeX file and return as a set.
    """
    titles = set()
    
    if not os.path.exists(bib_file_path):
        return titles
    
    with open(bib_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Split the content into individual entries
    entries = re.split(r'@\w+\{[^,]+,', content)[1:]
    
    for entry in entries:
        if not entry.strip():
            continue
            
        # Extract title
        title_match = re.search(r'title\s*=\s*\{([^}]+)\}', entry, re.IGNORECASE | re.DOTALL)
        if title_match:
            # Clean up the title (remove extra whitespace and newlines)
            title = ' '.join(title_match.group(1).strip().split())
            titles.add(title)
    
    return titles

def parse_icse_year(year, output_csv_path):
    """
    Parse all ICSE BibTeX files for a given year and create a CSV with artifact columns.
    """
    year_dir = os.path.join("data", str(year))
    base_file = os.path.join(year_dir, f"{year}ICSE.bib")
    
    if not os.path.exists(base_file):
        raise FileNotFoundError(f"Base file {base_file} not found")
    
    # Parse the base file to get all papers
    with open(base_file, 'r', encoding='utf-8') as file:
        content = file.read()
    
    entries = re.split(r'@\w+\{[^,]+,', content)[1:]
    papers = []
    
    for entry in entries:
        if not entry.strip():
            continue
            
        paper_data = {}
        
        # Extract title
        title_match = re.search(r'title\s*=\s*\{([^}]+)\}', entry, re.IGNORECASE | re.DOTALL)
        if title_match:
            paper_data['title'] = ' '.join(title_match.group(1).strip().split())
        else:
            paper_data['title'] = ''
        
        # Extract authors
        author_match = re.search(r'author\s*=\s*\{([^}]+)\}', entry, re.IGNORECASE | re.DOTALL)
        if author_match:
            authors = ' '.join(author_match.group(1).strip().split())
            authors = re.sub(r'\s+and\s+', ', ', authors)
            paper_data['authors'] = authors
        else:
            paper_data['authors'] = ''
        
        # Extract URL
        url_match = re.search(r'url\s*=\s*\{([^}]+)\}', entry, re.IGNORECASE)
        if url_match:
            paper_data['url'] = url_match.group(1).strip()
        else:
            paper_data['url'] = ''
        
        # Extract Abstract
        abs_match = re.search(r'abstract\s*=\s*\{([^}]+)\}', entry, re.IGNORECASE)
        if abs_match:
            paper_data['abstract'] = abs_match.group(1).strip()
        else:
            paper_data['abstract'] = ''
        
        if paper_data['title']:
            papers.append(paper_data)
    
    # Extract titles from artifact files
    available_titles = extract_titles_from_bib(os.path.join(year_dir, f"{year}ICSE_Artifact_Available.bib"))
    reusable_titles = extract_titles_from_bib(os.path.join(year_dir, f"{year}ICSE_Artifact_Reusable.bib"))
    functional_titles = extract_titles_from_bib(os.path.join(year_dir, f"{year}ICSE_Artifact_Functional.bib"))
    
    # Add artifact flags to papers
    for paper in papers:
        title = paper['title']
        paper['artifact_available'] = title in available_titles
        paper['artifact_reusable'] = title in reusable_titles
        paper['artifact_functional'] = title in functional_titles
    
    # Create output directory
    output_dir = os.path.dirname(output_csv_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    # Write to CSV
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'authors', 'url', 'abstract', 'artifact_available', 'artifact_reusable', 'artifact_functional']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for paper in papers:
            writer.writerow(paper)
    
    print(f"Successfully parsed {len(papers)} papers from {year} ICSE")
    print(f"Artifact statistics:")
    print(f"  Available: {len(available_titles)} papers")
    print(f"  Reusable: {len(reusable_titles)} papers")
    print(f"  Functional: {len(functional_titles)} papers")
    print(f"Results saved to {output_csv_path}")

def main():
    if len(sys.argv) == 3:
        # Original functionality: single BibTeX file
        input_file = sys.argv[1]
        output_filename = sys.argv[2]
        output_file = os.path.join("results", "bib", output_filename)
        
        try:
            parse_bibtex_file(input_file, output_file)
        except FileNotFoundError:
            print(f"Error: Could not find file '{input_file}'")
            sys.exit(1)
        except Exception as e:
            print(f"Error: {str(e)}")
            sys.exit(1)
    
    elif len(sys.argv) == 4 and sys.argv[1] == "--icse":
        # New functionality: ICSE year processing
        year = sys.argv[2]
        output_filename = sys.argv[3]
        output_file = os.path.join("results", "bib", output_filename)
        
        try:
            parse_icse_year(year, output_file)
        except FileNotFoundError as e:
            print(f"Error: {str(e)}")
            sys.exit(1)
        except Exception as e:
            print(f"Error: {str(e)}")
            sys.exit(1)
    
    else:
        print("Usage:")
        print("  Single file: python bib-converter.py <input_bib_file> <output_csv_file>")
        print("  ICSE year:   python bib-converter.py --icse <year> <output_csv_file>")
        print("")
        print("Examples:")
        print("  python bib-converter.py all-keywords.bib papers.csv")
        print("  python bib-converter.py --icse 2023 icse2023.csv")
        sys.exit(1)

if __name__ == "__main__":
    main()