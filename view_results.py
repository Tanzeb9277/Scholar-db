#!/usr/bin/env python3
"""
View Results - Display scraped books in a readable format

Usage:
    python3 view_results.py
"""

import json
import sys
from pathlib import Path


def view_results():
    """Display the scraped results in a readable format"""
    
    results_file = 'scholars_books.json'
    
    if not Path(results_file).exists():
        print(f"❌ Results file not found: {results_file}")
        print("\nRun one of the scrapers first:")
        print("  python3 scraper_undetected.py")
        print("  python3 scraper_playwright.py")
        print("  python3 scraper.py")
        sys.exit(1)
    
    try:
        with open(results_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Error reading {results_file}: {e}")
        sys.exit(1)
    
    if not data:
        print(f"📭 No results found in {results_file}")
        sys.exit(0)
    
    # Display results
    print("=" * 100)
    print(f"📚 ISLAMIC SCHOLARS BOOKS DATABASE")
    print("=" * 100)
    print()
    
    total_books = 0
    total_scholars = len(data)
    
    for scholar_name, scholar_data in data.items():
        death_year = scholar_data.get('death_year_hijri', 'N/A')
        url = scholar_data.get('url', 'N/A')
        books = scholar_data.get('books', [])
        
        print(f"🎓 {scholar_name} (d. {death_year}H)")
        print(f"   📎 {url}")
        print(f"   📖 {len(books)} book(s)")
        print()
        
        if books:
            for i, book in enumerate(books, 1):
                english = book.get('english_title', 'N/A')
                arabic = book.get('arabic_title', 'N/A')
                
                print(f"   {i}. {english}")
                if arabic and arabic != 'N/A':
                    print(f"      {arabic}")
                print()
            
            total_books += len(books)
        else:
            print("      ⚠️  No books found")
            print()
        
        print("-" * 100)
        print()
    
    # Summary
    print("=" * 100)
    print(f"📊 SUMMARY")
    print("=" * 100)
    print(f"   Total Scholars: {total_scholars}")
    print(f"   Total Books: {total_books}")
    print(f"   Average Books per Scholar: {total_books / total_scholars if total_scholars > 0 else 0:.1f}")
    print("=" * 100)


def export_csv():
    """Export results to CSV format"""
    
    results_file = 'scholars_books.json'
    output_file = 'scholars_books.csv'
    
    if not Path(results_file).exists():
        print(f"❌ Results file not found: {results_file}")
        sys.exit(1)
    
    try:
        with open(results_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Error reading {results_file}: {e}")
        sys.exit(1)
    
    # Create CSV
    import csv
    
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Scholar Name', 'Death Year (H)', 'English Title', 'Arabic Title', 'URL'])
        
        for scholar_name, scholar_data in data.items():
            death_year = scholar_data.get('death_year_hijri', '')
            url = scholar_data.get('url', '')
            books = scholar_data.get('books', [])
            
            if books:
                for book in books:
                    writer.writerow([
                        scholar_name,
                        death_year,
                        book.get('english_title', ''),
                        book.get('arabic_title', ''),
                        url
                    ])
            else:
                writer.writerow([scholar_name, death_year, '', '', url])
    
    print(f"✅ Exported to {output_file}")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--csv':
        export_csv()
    else:
        view_results()


if __name__ == "__main__":
    main()
