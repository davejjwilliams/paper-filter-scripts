import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import json
from urllib.parse import urljoin, urlparse
import logging
import argparse
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PaperScraper:
    def __init__(self, base_url):
        """
        Initialize the scraper
        
        Args:
            base_url (str): The website URL to scrape
            delay (int): Delay between requests in seconds
        """
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.papers = []
    
    def fetch_page(self, url):
        """
        Fetch a web page with error handling
        
        Args:
            url (str): URL to fetch
            
        Returns:
            BeautifulSoup object or None if failed
        """
        try:
            logger.info(f"Fetching: {url}")
            response = self.session.get(url, timeout=2)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def extract_paper_info(self, paper_element):
        """
        Extract information from a single paper element (table row)
        
        Args:
            paper_element: BeautifulSoup element containing paper info (tr element)
            
        Returns:
            dict: Paper information
        """
        paper_info = {
            'title': '',
            'authors': '',
        }
        
        # The paper is in the second td element of the tr
        td_elements = paper_element.find_all('td')
        if len(td_elements) >= 2:
            paper_content = td_elements[1]  # Second td element
            
            # Titles are links 
            title_elem = (
                paper_content.find('a')
            )
            if title_elem:
                paper_info['title'] = title_elem.get_text(strip=True)
            
            # Authors are in a div with class 'performers'
            authors_elem = (
                paper_content.find('div', class_='performers')
            )
            if authors_elem:
                paper_info['authors'] = authors_elem.get_text(strip=True)
            
            all_text = paper_content.get_text(separator=' | ', strip=True)
            logger.debug(f"Paper content: {all_text}")
        
        return paper_info
    
    def scrape_papers(self, max_pages=None):
        """
        Main scraping method - modified for table-based structure
        
        Args:
            max_pages (int): Maximum number of pages to scrape (None for all)
        """
        soup = self.fetch_page(self.base_url)
        if not soup:
            logger.error("Failed to fetch the main page")
            return
        
        # Find all table rows that contain papers
        # Look for tr elements within tables
        paper_elements = soup.find_all('tr')
        
        # Filter out header rows and empty rows
        # Valid rows should have at least 2 td elements, with the second one not empty
        valid_papers = []
        for tr in paper_elements:
            td_elements = tr.find_all('td')
            if len(td_elements) >= 2:
                second_td = td_elements[1]
                if second_td.get_text(strip=True):
                    valid_papers.append(tr)
        
        if not valid_papers:
            logger.warning("No paper rows found")
            return
        
        logger.info(f"Found {len(valid_papers)} potential paper rows")
        
        for paper_elem in valid_papers:
            paper_info = self.extract_paper_info(paper_elem)
            if paper_info['title']:
                self.papers.append(paper_info)
                logger.info(f"Extracted: {paper_info['title']}...")
        
        logger.info(f"Total papers scraped: {len(self.papers)}")
    
    def save_to_csv(self, filename):
        """Save scraped papers to CSV file"""
        os.makedirs('results/researchr', exist_ok=True)
        if self.papers:
            df = pd.DataFrame(self.papers)
            df.to_csv(f"results/researchr/{filename}", index=False)
            logger.info(f"Saved {len(self.papers)} papers to results/researchr/{filename}")
        else:
            logger.warning("No papers to save")
    
    def save_to_json(self, filename):
        """Save scraped papers to JSON file"""
        os.makedirs('results/researchr', exist_ok=True)
        if self.papers:
            with open(f"results/researchr/{filename}", 'w', encoding='utf-8') as f:
                json.dump(self.papers, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {len(self.papers)} papers to results/researchr/{filename}")
        else:
            logger.warning("No papers to save")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape academic papers from a conference website')
    parser.add_argument('url', help='Target website URL to scrape')
    parser.add_argument('year', help='Year of the conference (e.g., 2023)')
    
    args = parser.parse_args()
    
    scraper = PaperScraper(args.url)
    scraper.scrape_papers()
    scraper.save_to_csv(f"{args.year}_papers.csv")