#!/usr/bin/env python3
"""
Islamic Scholars Books Scraper
Scrapes book information from sifatusafwa.com for a list of scholars
"""

import json
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import time
import sys


def scrape_scholar_books(scholar_name: str, death_year: str) -> List[Dict[str, str]]:
    """
    Scrape books for a given scholar from sifatusafwa.com
    
    Args:
        scholar_name: Name of the scholar (formatted for URL, e.g., 'imam-malik')
        death_year: Hijri death year (e.g., '179')
    
    Returns:
        List of dictionaries containing book information
    """
    # Construct the URL
    url = f"https://www.sifatusafwa.com/en/manufacturer/{scholar_name}-{death_year}h.html"
    
    print(f"Scraping {scholar_name} ({death_year}H)...")
    print(f"URL: {url}")
    
    try:
        # Send GET request with comprehensive headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,ar;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'Referer': 'https://www.sifatusafwa.com/'
        }
        
        # Create a session to maintain cookies
        session = requests.Session()
        
        # First visit the homepage to get cookies
        session.get('https://www.sifatusafwa.com/', headers=headers, timeout=30)
        time.sleep(2)
        
        # Then visit the scholar page
        response = session.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all product items
        products = soup.find_all('div', class_='js-product-miniature')
        
        books = []
        for product in products:
            # Extract English title
            title_elem = product.find('h2', class_='product-title')
            if title_elem and title_elem.find('a'):
                english_title = title_elem.find('a').get_text(strip=True)
            else:
                english_title = None
            
            # Extract Arabic title
            subtitle_elem = product.find('div', class_='product-subtitle')
            arabic_title = subtitle_elem.get_text(strip=True) if subtitle_elem else None
            
            # Only add if we have at least one title
            if english_title or arabic_title:
                books.append({
                    'english_title': english_title,
                    'arabic_title': arabic_title
                })
        
        print(f"  Found {len(books)} book(s)")
        return books
        
    except requests.exceptions.RequestException as e:
        print(f"  Error fetching data: {e}")
        return []
    except Exception as e:
        print(f"  Error parsing data: {e}")
        return []


def main():
    """Main function to scrape all scholars and save to JSON"""
    
    # Load scholars list
    try:
        with open('scholars.json', 'r', encoding='utf-8') as f:
            scholars = json.load(f)
    except FileNotFoundError:
        print("Error: scholars.json file not found!")
        print("Please create a scholars.json file with the list of scholars.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing scholars.json: {e}")
        sys.exit(1)
    
    # Dictionary to store results
    results = {}
    
    # Scrape each scholar
    for scholar in scholars:
        scholar_name = scholar.get('name')
        death_year = scholar.get('death_year')
        url_name = scholar.get('url_name')
        
        if not url_name or not death_year:
            print(f"Warning: Skipping {scholar_name} - missing url_name or death_year")
            continue
        
        # Scrape books for this scholar
        books = scrape_scholar_books(url_name, death_year)
        
        # Store in results
        results[scholar_name] = {
            'death_year_hijri': death_year,
            'url': f"https://www.sifatusafwa.com/en/manufacturer/{url_name}-{death_year}h.html",
            'books': books
        }
        
        # Be polite - add delay between requests
        time.sleep(1)
    
    # Save results to JSON
    output_file = 'scholars_books.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Scraping complete! Results saved to {output_file}")
    
    # Print summary
    total_books = sum(len(scholar['books']) for scholar in results.values())
    print(f"📚 Total scholars: {len(results)}")
    print(f"📖 Total books: {total_books}")


if __name__ == "__main__":
    main()
