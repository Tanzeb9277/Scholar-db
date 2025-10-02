#!/usr/bin/env python3
"""
Islamic Scholars Book Scraper (Playwright version)
Scrapes book information from sifatusafwa.com for a list of scholars
Uses Playwright to handle bot protection
"""

import json
import time
import sys
from typing import List, Dict
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout


class ScholarBookScraper:
    def __init__(self, base_url: str = "https://www.sifatusafwa.com/en/manufacturer"):
        self.base_url = base_url
    
    def construct_url(self, scholar_name: str, hijri_year: str) -> str:
        """Construct the URL for a scholar's page"""
        return f"{self.base_url}/{scholar_name}-{hijri_year}h.html"
    
    def scrape_books(self, page, url: str) -> List[Dict[str, str]]:
        """Scrape book information from a scholar's page"""
        books = []
        
        try:
            print(f"Fetching: {url}")
            # Try to load the page with a more lenient wait strategy
            try:
                page.goto(url, wait_until='domcontentloaded', timeout=60000)
            except PlaywrightTimeout:
                print(f"  Timeout loading page, trying with load strategy")
                page.goto(url, wait_until='load', timeout=60000)
            
            # Wait a bit for JavaScript to execute
            page.wait_for_timeout(3000)
            
            # Wait for products to load
            try:
                page.wait_for_selector('article.product-miniature', timeout=10000)
            except PlaywrightTimeout:
                print(f"  No products found on page")
                return books
            
            # Find all product articles
            products = page.query_selector_all('article.product-miniature')
            
            for product in products:
                # Extract English name from product-title
                title_element = product.query_selector('h2.product-title a')
                english_name = title_element.inner_text().strip() if title_element else ""
                
                # Extract Arabic name from product-subtitle
                subtitle_element = product.query_selector('div.product-subtitle')
                arabic_name = subtitle_element.inner_text().strip() if subtitle_element else ""
                
                # Only add if we found at least one name
                if english_name or arabic_name:
                    books.append({
                        'english_name': english_name,
                        'arabic_name': arabic_name
                    })
            
            print(f"  Found {len(books)} books")
            
        except PlaywrightTimeout as e:
            print(f"  Timeout error fetching {url}: {e}", file=sys.stderr)
        except Exception as e:
            print(f"  Error fetching/parsing {url}: {e}", file=sys.stderr)
        
        return books
    
    def scrape_scholars(self, scholars_file: str, output_file: str, headless: bool = True):
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
        
        # Use Playwright to scrape
        with sync_playwright() as p:
            # Launch browser
            browser = p.chromium.launch(headless=headless)
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            page = context.new_page()
            
            # Scrape each scholar
            for scholar in scholars:
                name = scholar.get('name', '')
                hijri_year = scholar.get('hijri_year', '')
                
                if not name or not hijri_year:
                    print(f"Skipping invalid scholar entry: {scholar}", file=sys.stderr)
                    continue
                
                url = self.construct_url(name, hijri_year)
                books = self.scrape_books(page, url)
                
                results[name] = {
                    'hijri_year': hijri_year,
                    'url': url,
                    'books': books,
                    'book_count': len(books)
                }
                
                # Be polite - add a small delay between requests
                time.sleep(2)
            
            # Close browser
            browser.close()
        
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
    scraper.scrape_scholars(scholars_file, output_file, headless=True)


if __name__ == '__main__':
    main()
