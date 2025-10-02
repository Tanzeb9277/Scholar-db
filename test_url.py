#!/usr/bin/env python3
"""
URL Tester - Test if a scholar URL is valid and shows books

Usage:
    python3 test_url.py imam-malik 179
    
This will test: https://www.sifatusafwa.com/en/manufacturer/imam-malik-179h.html
"""

import sys
import requests

def test_url(url_name, death_year):
    """Test if a URL is accessible and likely has content"""
    
    url = f"https://www.sifatusafwa.com/en/manufacturer/{url_name}-{death_year}h.html"
    
    print(f"Testing URL: {url}")
    print("-" * 80)
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
        
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        
        print(f"Status Code: {response.status_code}")
        print(f"Final URL: {response.url}")
        print(f"Content Length: {len(response.content)} bytes")
        
        # Check for common indicators
        content = response.text.lower()
        
        if 'cloudflare' in content or 'just a moment' in content:
            print("\n⚠️  Cloudflare protection detected")
            print("   This is expected. The scraper tools will handle this.")
        
        if response.status_code == 404:
            print("\n❌ URL not found (404)")
            print("   Check the url_name and death_year are correct")
        elif response.status_code == 200:
            print("\n✅ URL is accessible")
            
            if 'product' in content:
                print("   Page likely contains products")
            else:
                print("   ⚠️  No products detected (might be empty or blocked)")
        
        # Generate JSON entry
        print("\n" + "=" * 80)
        print("Add this to scholars.json:")
        print("=" * 80)
        print("{")
        print(f'  "name": "Scholar Name Here",')
        print(f'  "url_name": "{url_name}",')
        print(f'  "death_year": "{death_year}"')
        print("}")
        print("=" * 80)
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error: {e}")
        return False
    
    return True


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 test_url.py <url_name> <death_year>")
        print("\nExample:")
        print("  python3 test_url.py imam-malik 179")
        print("\nThis tests: https://www.sifatusafwa.com/en/manufacturer/imam-malik-179h.html")
        sys.exit(1)
    
    url_name = sys.argv[1]
    death_year = sys.argv[2]
    
    test_url(url_name, death_year)


if __name__ == "__main__":
    main()
