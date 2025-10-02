#!/usr/bin/env python3
"""
Islamic Scholars Books Scraper (Playwright version)
Scrapes book information from sifatusafwa.com for a list of scholars
Uses Playwright to handle JavaScript and anti-bot protection
"""

import json
import asyncio
from playwright.async_api import async_playwright
from typing import List, Dict
import sys


async def scrape_scholar_books(page, scholar_name: str, death_year: str) -> List[Dict[str, str]]:
    """
    Scrape books for a given scholar from sifatusafwa.com
    
    Args:
        page: Playwright page object
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
        # Navigate to the page with a more lenient wait
        await page.goto(url, wait_until='domcontentloaded', timeout=30000)
        
        # Wait a bit for JavaScript to execute
        await asyncio.sleep(3)
        
        # Wait for products to load (or timeout gracefully)
        try:
            await page.wait_for_selector('.js-product-miniature', timeout=10000)
        except Exception:
            # If products don't load, check if page has content
            print(f"  Warning: Products selector not found, checking page content...")
        
        # Save page content for debugging
        content = await page.content()
        with open(f'debug_{scholar_name}.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Page content saved to debug_{scholar_name}.html")
        
        # Extract book information
        books = await page.evaluate('''() => {
            const products = document.querySelectorAll('.js-product-miniature');
            const books = [];
            
            products.forEach(product => {
                // Extract English title
                const titleElem = product.querySelector('h2.product-title a');
                const englishTitle = titleElem ? titleElem.textContent.trim() : null;
                
                // Extract Arabic title
                const subtitleElem = product.querySelector('.product-subtitle');
                const arabicTitle = subtitleElem ? subtitleElem.textContent.trim() : null;
                
                // Only add if we have at least one title
                if (englishTitle || arabicTitle) {
                    books.push({
                        english_title: englishTitle,
                        arabic_title: arabicTitle
                    });
                }
            });
            
            return books;
        }''')
        
        print(f"  Found {len(books)} book(s)")
        return books
        
    except Exception as e:
        print(f"  Error: {e}")
        return []


async def main():
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
    
    # Start Playwright
    async with async_playwright() as p:
        # Launch browser in headless mode
        browser = await p.chromium.launch(headless=True)
        
        # Create a new browser context
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080},
            locale='en-US'
        )
        
        # Create a new page
        page = await context.new_page()
        
        # Scrape each scholar
        for scholar in scholars:
            scholar_name = scholar.get('name')
            death_year = scholar.get('death_year')
            url_name = scholar.get('url_name')
            
            if not url_name or not death_year:
                print(f"Warning: Skipping {scholar_name} - missing url_name or death_year")
                continue
            
            # Scrape books for this scholar
            books = await scrape_scholar_books(page, url_name, death_year)
            
            # Store in results
            results[scholar_name] = {
                'death_year_hijri': death_year,
                'url': f"https://www.sifatusafwa.com/en/manufacturer/{url_name}-{death_year}h.html",
                'books': books
            }
            
            # Be polite - add delay between requests
            await asyncio.sleep(2)
        
        # Close browser
        await browser.close()
    
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
    asyncio.run(main())
