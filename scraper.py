#!/usr/bin/env python3
"""
Islamic Scholars Book Scraper
Scrapes book information from sifatusafwa.com for a list of scholars
"""

import json
import time
import sys
from typing import List, Dict
import requests
from bs4 import BeautifulSoup


class ScholarBookScraper:
    def __init__(self, base_url: str = "https://www.sifatusafwa.com/en/manufacturer"):
        self.base_url = base_url
        self.session = requests.Session()
        # Add comprehensive headers to mimic a real browser
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        })
    
    def construct_url(self, scholar_name: str, hijri_year: str) -> str:
        """Construct the URL for a scholar's page"""
        return f"{self.base_url}/{scholar_name}-{hijri_year}h.html"
    
    def scrape_books(self, url: str) -> List[Dict[str, str]]:
        """Scrape book information from a scholar's page"""
        books = []
        
        try:
            print(f"Fetching: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all product articles
            products = soup.find_all('article', class_='product-miniature')
            
            for product in products:
                # Extract English name from product-title
                title_element = product.find('h2', class_='product-title')
                if title_element:
                    title_link = title_element.find('a')
                    english_name = title_link.text.strip() if title_link else ""
                else:
                    english_name = ""
                
                # Extract Arabic name from product-subtitle
                subtitle_element = product.find('div', class_='product-subtitle')
                arabic_name = subtitle_element.text.strip() if subtitle_element else ""
                
                # Only add if we found at least one name
                if english_name or arabic_name:
                    books.append({
                        'english_name': english_name,
                        'arabic_name': arabic_name
                    })
            
            print(f"  Found {len(books)} books")
            
        except requests.exceptions.RequestException as e:
            print(f"  Error fetching {url}: {e}", file=sys.stderr)
        except Exception as e:
            print(f"  Error parsing {url}: {e}", file=sys.stderr)
        
        return books
    
    def scrape_scholars(self, scholars_file: str, output_file: str):
        """Scrape books for all scholars in the input file"""
        # Load scholars list
        try:
            with open(scholars_file, 'r', encoding='utf-8') as f:
                scholars = json.load(f)
        except FileNotFoundError:
            print(f"Error: File '{scholars_file}' not found", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in '{scholars_file}': {e}", file=sys.stderr)
            sys.exit(1)
        
        print(f"Loaded {len(scholars)} scholars from {scholars_file}\n")
        
        # Results dictionary
        results = {}
        
        # Scrape each scholar
        for scholar in scholars:
            name = scholar.get('name', '')
            hijri_year = scholar.get('hijri_year', '')
            
            if not name or not hijri_year:
                print(f"Skipping invalid scholar entry: {scholar}", file=sys.stderr)
                continue
            
            url = self.construct_url(name, hijri_year)
            books = self.scrape_books(url)
            
            results[name] = {
                'hijri_year': hijri_year,
                'url': url,
                'books': books,
                'book_count': len(books)
            }
            
            # Be polite - add a small delay between requests
            time.sleep(2)
        
        # Save results to JSON file
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"\nResults saved to {output_file}")
            
            # Print summary
            total_books = sum(scholar_data['book_count'] for scholar_data in results.values())
            print(f"\nSummary:")
            print(f"  Scholars processed: {len(results)}")
            print(f"  Total books found: {total_books}")
            
        except Exception as e:
            print(f"Error saving results: {e}", file=sys.stderr)
            sys.exit(1)


def main():
    """Main entry point"""
    scholars_file = 'scholars.json'
    output_file = 'books_output.json'
    
    scraper = ScholarBookScraper()
    scraper.scrape_scholars(scholars_file, output_file)


if __name__ == '__main__':
    main()
