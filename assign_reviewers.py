import csv
import sys
from math import ceil

def assign_reviewers(input_file, output_file, reviewer_initials):
    """
    Filter papers with ai=True and assign them evenly to reviewers.
    
    Args:
        input_file (str): Path to input CSV file
        output_file (str): Path to output CSV file
        reviewer_initials (list): List of reviewer initials
    """
    # Read and filter papers
    filtered_papers = []
    
    with open(input_file, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        
        for row in reader:
            # Filter papers where ai column is True
            if row['ai'].lower() == 'true':
                filtered_papers.append(row)
    
    # Calculate papers per reviewer
    total_papers = len(filtered_papers)
    num_reviewers = len(reviewer_initials)
    
    if total_papers == 0:
        print("No papers with ai=True found.")
        return
    
    papers_per_reviewer = ceil(total_papers / num_reviewers)
    
    # Assign reviewers
    assigned_papers = []
    for i, paper in enumerate(filtered_papers):
        reviewer_index = i // papers_per_reviewer
        if reviewer_index >= num_reviewers:
            reviewer_index = num_reviewers - 1
        
        # Create new row with reviewer and relevant columns at the beginning
        new_row = {
            'reviewer': reviewer_initials[reviewer_index],
            'relevant': '',  # Empty initially
            'title': paper['title'],
            'authors': paper['authors'],
            'url': paper['url'],
            'abstract': paper['abstract'],
            'artifact_available': paper['artifact_available'],
            'artifact_reusable': paper['artifact_reusable'],
            'artifact_functional': paper['artifact_functional'],
            'ai': paper['ai']
        }
        assigned_papers.append(new_row)
    
    # Write to output file
    fieldnames = ['reviewer', 'relevant', 'title', 'authors', 'url', 'abstract', 
                  'artifact_available', 'artifact_reusable', 'artifact_functional', 'ai']
    
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(assigned_papers)
    
    print(f"Assigned {total_papers} papers to {num_reviewers} reviewers.")
    print(f"Output written to: {output_file}")
    
    # Print assignment summary
    for i, initials in enumerate(reviewer_initials):
        start_idx = i * papers_per_reviewer
        end_idx = min((i + 1) * papers_per_reviewer, total_papers)
        count = end_idx - start_idx
        print(f"{initials}: {count} papers")

def main():
    if len(sys.argv) != 4:
        print("Usage: python assign_reviewers.py <input_csv> <output_csv> <reviewer_initials>")
        print("Example: python assign_reviewers.py papers.csv assigned_papers.csv DW,AA,JP,FS")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    reviewer_initials = [initial.strip() for initial in sys.argv[3].split(',')]
    
    try:
        assign_reviewers(input_file, output_file, reviewer_initials)
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()