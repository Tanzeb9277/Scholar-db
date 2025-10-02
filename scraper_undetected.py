#!/usr/bin/env python3
"""
Islamic Scholars Books Scraper (Undetected ChromeDriver version)
Uses undetected-chromedriver to bypass Cloudflare protection
"""

import json
import time
import sys
from typing import List, Dict

try:
    import undetected_chromedriver as uc
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
except ImportError:
    print("Error: Required packages not installed!")
    print("Please run: pip install undetected-chromedriver selenium")
    sys.exit(1)


def scrape_scholar_books(driver, scholar_name: str, death_year: str) -> List[Dict[str, str]]:
    """
    Scrape books for a given scholar from sifatusafwa.com
    
    Args:
        driver: Selenium WebDriver instance
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
        # Navigate to the page
        driver.get(url)
        
        # Wait for Cloudflare challenge to complete (if present)
        print("  Waiting for page to load (Cloudflare may take 5-10 seconds)...")
        time.sleep(10)
        
        # Wait for products to load
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "js-product-miniature"))
            )
        except Exception:
            print("  Warning: Products not found, checking page...")
        
        # Extract book information
        books = []
        products = driver.find_elements(By.CLASS_NAME, "js-product-miniature")
        
        for product in products:
            try:
                # Extract English title
                title_elem = product.find_element(By.CSS_SELECTOR, "h2.product-title a")
                english_title = title_elem.text.strip() if title_elem else None
            except Exception:
                english_title = None
            
            try:
                # Extract Arabic title
                subtitle_elem = product.find_element(By.CLASS_NAME, "product-subtitle")
                arabic_title = subtitle_elem.text.strip() if subtitle_elem else None
            except Exception:
                arabic_title = None
            
            # Only add if we have at least one title
            if english_title or arabic_title:
                books.append({
                    'english_title': english_title,
                    'arabic_title': arabic_title
                })
        
        print(f"  Found {len(books)} book(s)")
        return books
        
    except Exception as e:
        print(f"  Error: {e}")
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
    
    # Initialize undetected Chrome driver
    print("Initializing browser...")
    options = uc.ChromeOptions()
    
    # Uncomment the line below to run in headless mode (no visible browser)
    # options.add_argument('--headless=new')
    
    driver = uc.Chrome(options=options)
    
    try:
        # Scrape each scholar
        for scholar in scholars:
            scholar_name = scholar.get('name')
            death_year = scholar.get('death_year')
            url_name = scholar.get('url_name')
            
            if not url_name or not death_year:
                print(f"Warning: Skipping {scholar_name} - missing url_name or death_year")
                continue
            
            # Scrape books for this scholar
            books = scrape_scholar_books(driver, url_name, death_year)
            
            # Store in results
            results[scholar_name] = {
                'death_year_hijri': death_year,
                'url': f"https://www.sifatusafwa.com/en/manufacturer/{url_name}-{death_year}h.html",
                'books': books
            }
            
            # Be polite - add delay between requests
            time.sleep(3)
        
    finally:
        # Close browser
        driver.quit()
    
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
