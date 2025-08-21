import pandas as pd
import ollama
import time
import argparse
from typing import Optional

def extract_country_with_llm(affiliation: str, model: str = 'gemma3:4b') -> Optional[str]:
    if pd.isna(affiliation) or not isinstance(affiliation, str):
        return None
    
    prompt = f"""
    Get the country from this academic affiliation. Return only the country name, nothing else.
    
    Affiliation: {affiliation}
    
    Country:"""
    
    try:
        response = ollama.chat(
            model=model,
            messages=[{'role': 'user', 'content': prompt}],
            options={'temperature': 0}  # For consistent results
        )
        
        country = response['message']['content'].strip()
        
        # Clean up common variations
        country_mapping = {
            'USA': 'United States',
            'US': 'United States',
            'United States of America': 'United States',
            'UK': 'United Kingdom',
        }
        
        return country_mapping.get(country, country)
        
    except Exception as e:
        print(f"Error processing affiliation: {affiliation[:50]}... - {e}")
        return "Error"

def process_affiliations_csv(input_file: str, output_file: str = None, model: str = 'gemma3:4b'):
    """
    Process CSV file to add country column using LLM extraction.
    """

    df = pd.read_csv(input_file)
    
    print(f"Processing {len(df)} rows...")
    
    if 'country' in df.columns:
        print("Country column already exists. Updating missing values only.")
        mask = df['country'].isna() | (df['country'] == '')
        df_to_process = df[mask]
    else:
        print("Adding new country column.")
        df['country'] = None
        df_to_process = df
    
    # Process each unique affiliation to avoid redundant LLM calls
    unique_affiliations = df_to_process['affiliations'].dropna().unique()
    
    print(f"Processing {len(unique_affiliations)} unique affiliations...")
    
    affiliation_to_country = {}
    
    for i, affiliation in enumerate(unique_affiliations):
        print(f"Progress: {i}/{len(unique_affiliations)} ({i/len(unique_affiliations)*100:.1f}%)")
        
        country = extract_country_with_llm(affiliation, model)
        affiliation_to_country[affiliation] = country
    
    # Map countries back to dataframe
    df['country'] = df['affiliations'].map(affiliation_to_country).fillna(df['country'])
    
    if output_file is None:
        output_file = input_file.replace('.csv', '_with_countries.csv')
    
    df.to_csv(output_file, index=False)
    print(f"Results saved to {output_file}")
    
    # Print summary
    print("\nCountry distribution:")
    print(df['country'].value_counts().head(15))
    
    return df

def main():
    parser = argparse.ArgumentParser(description='Extract countries from academic affiliations using local LLM')
    parser.add_argument('input', help='Input CSV file path')
    parser.add_argument('-o', '--output', help='Output CSV file path (optional)')
    parser.add_argument('--model', default='gemma3:4b', help='Ollama model to use (default: gemma3:4b)')

    args = parser.parse_args()
    
    process_affiliations_csv(args.input, args.output, args.model)

if __name__ == "__main__":
    main()