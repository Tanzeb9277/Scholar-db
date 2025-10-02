# Islamic Scholars Book Scraper

## Overview
This project scrapes book information (English and Arabic titles) for Islamic scholars from sifatusafwa.com.

## Files

- **`scholars.json`** - Input file containing the list of scholars
- **`scraper.py`** - Basic scraper using requests and BeautifulSoup
- **`scraper_playwright.py`** - Advanced scraper using Playwright (handles JavaScript)
- **`books_output.json`** - Output file with scraped book data
- **`requirements.txt`** - Python dependencies

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Install Playwright browsers (only needed for `scraper_playwright.py`):
   ```bash
   python3 -m playwright install chromium
   ```

## Usage

### 1. Edit the Scholars List

Edit `scholars.json` to add your scholars. Format:

```json
[
  {
    "name": "imam-malik",
    "hijri_year": "179"
  },
  {
    "name": "imam-bukhari",
    "hijri_year": "256"
  }
]
```

**Important**: The `name` field should be URL-friendly (lowercase, hyphens instead of spaces).

### 2. Run the Scraper

Using Playwright (recommended):
```bash
python3 scraper_playwright.py
```

Using requests (simpler but less effective):
```bash
python3 scraper.py
```

### 3. View Results

Check `books_output.json` for the scraped data. Format:

```json
{
  "imam-malik": {
    "hijri_year": "179",
    "url": "https://www.sifatusafwa.com/en/manufacturer/imam-malik-179h.html",
    "books": [
      {
        "english_name": "Al-Muwatta by Imam Malik",
        "arabic_name": "الموطأ للإمام مالك"
      }
    ],
    "book_count": 1
  }
}
```

## Known Issues

### Cloudflare Protection 🛡️

**The website uses Cloudflare's anti-bot protection** which blocks automated scraping tools. When you try to access the site programmatically, you'll see a "Just a moment..." verification page instead of the actual content.

#### Symptoms:
- Page title: "Just a moment..."
- No products found
- 403 Forbidden errors (with basic scraper)
- Timeout or empty results (with Playwright)

#### Workarounds:

1. **Manual Data Entry** (Most Reliable)
   - Visit the URLs manually in your browser
   - Copy book titles and paste into a text file
   - Process into JSON format

2. **Browser Automation with Human Interaction**
   - Run Playwright in non-headless mode (GUI browser)
   - Manually solve the Cloudflare challenge
   - Then let the script continue
   
   Modify `scraper_playwright.py`:
   ```python
   scraper.scrape_scholars(scholars_file, output_file, headless=False)
   ```
   
   Then manually click through the Cloudflare challenge when the browser opens.

3. **CAPTCHA Solving Services** (Paid)
   - Services like 2Captcha, Anti-Captcha
   - Integrate their API to solve Cloudflare challenges
   - Requires payment and additional coding

4. **Use Official APIs** (If Available)
   - Check if sifatusafwa.com offers an official API
   - Contact them about data access for research purposes

5. **Alternative Data Sources**
   - Look for other websites that list the same books
   - Academic databases or library catalogs
   - Islamic scholarly databases

## Troubleshooting

**Q: The scraper runs but finds 0 books**  
A: This is due to Cloudflare protection. See "Workarounds" above.

**Q: I get 403 Forbidden errors**  
A: The website is blocking automated requests. Try the Playwright version or manual methods.

**Q: Can I bypass Cloudflare?**  
A: It's very difficult and may violate the website's terms of service. Consider alternative approaches.

## Ethical Considerations

- Respect the website's `robots.txt` and terms of service
- Don't overwhelm the server with rapid requests
- Consider reaching out to the website administrators for permission
- Use scraped data responsibly and ethically

## License

This is a personal tool for data collection. Ensure you have permission before scraping any website.
