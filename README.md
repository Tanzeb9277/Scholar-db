# Islamic Scholars Books Database

A project to scrape and catalog books by Islamic scholars from sifatusafwa.com.

## ⚠️ Important Note: Cloudflare Protection

The website (`sifatusafwa.com`) is protected by **Cloudflare's bot detection** system, which prevents automated scraping. When you try to access the pages programmatically, you'll encounter a "Verify you are human" challenge page.

## Files Included

1. **`scholars.json`** - List of scholars to scrape (you need to populate this)
2. **`scraper_undetected.py`** - **RECOMMENDED** - Uses undetected-chromedriver (best success rate)
3. **`scraper_playwright.py`** - Browser-based scraper using Playwright
4. **`scraper.py`** - Basic scraper using requests/BeautifulSoup
5. **`test_url.py`** - Helper tool to test if a scholar URL is valid
6. **`view_results.py`** - View scraped results in readable format (also exports to CSV)
7. **`requirements.txt`** - Python dependencies
8. **`USAGE.md`** - Detailed usage instructions
9. **`PROJECT_SUMMARY.md`** - Complete project overview

## Quick Start

See **[USAGE.md](USAGE.md)** for detailed step-by-step instructions.

### TL;DR

```bash
# Install dependencies
pip install -r requirements.txt
pip install undetected-chromedriver selenium

# Edit scholars.json with your scholars list

# Run the best scraper (opens browser window)
python3 scraper_undetected.py
```

## Full Setup

```bash
pip install -r requirements.txt

# For Playwright version:
playwright install chromium

# For undetected-chromedriver (RECOMMENDED):
pip install undetected-chromedriver selenium
```

## How to Use

### Step 1: Populate the Scholars List

Edit `scholars.json` and add your scholars in this format:

```json
[
  {
    "name": "Imam Malik",
    "url_name": "imam-malik",
    "death_year": "179"
  },
  {
    "name": "Imam Ahmad",
    "url_name": "imam-ahmad",
    "death_year": "241"
  }
]
```

**How to find the correct values:**
- Visit: `https://www.sifatusafwa.com/en/manufacturer/[url_name]-[death_year]h.html`
- Example: `https://www.sifatusafwa.com/en/manufacturer/imam-malik-179h.html`
- `url_name`: The name part in the URL (e.g., "imam-malik")
- `death_year`: The hijri year of death (e.g., "179")

### Step 2: Run the Scraper

```bash
# Try the basic scraper
python3 scraper.py

# Or try the Playwright version
python3 scraper_playwright.py
```

**Note:** Due to Cloudflare protection, both scrapers will likely fail or return no results.

## Workarounds for Cloudflare Protection

Since automated scraping is blocked, here are some alternatives:

### Option 1: Manual Browser Extension
Use a browser extension like "Web Scraper" or "Data Miner" to manually extract data while browsing.

### Option 2: Undetected ChromeDriver (Recommended)
I've included `scraper_undetected.py` which uses `undetected-chromedriver` to bypass Cloudflare:

```bash
# Install additional dependencies
pip install undetected-chromedriver selenium

# Run the scraper (a browser window will open)
python3 scraper_undetected.py
```

This opens a real Chrome browser and waits for Cloudflare to complete. It has the best chance of success.

### Option 3: Cloudflare Bypass Services
Use a service like:
- **ScraperAPI** (https://www.scraperapi.com/)
- **Bright Data** (https://brightdata.com/)
- **Oxylabs** (https://oxylabs.io/)

These services handle Cloudflare challenges for you (paid services).

### Option 4: Manual Collection
1. Visit each scholar page manually
2. Copy the HTML
3. Save to files
4. Run a modified version of the scraper on local files

### Option 5: Contact the Website
Reach out to sifatusafwa.com and ask if they have an API or bulk export option for research purposes.

## Output Format

When successful, the scraper creates `scholars_books.json`:

```json
{
  "Imam Malik": {
    "death_year_hijri": "179",
    "url": "https://www.sifatusafwa.com/en/manufacturer/imam-malik-179h.html",
    "books": [
      {
        "english_title": "Al-Muwatta by Imam Malik",
        "arabic_title": "الموطأ للإمام مالك"
      }
    ]
  }
}
```

## HTML Structure Reference

For manual scraping or modifications, the relevant HTML structure is:

```html
<div class="js-product-miniature" data-id-product="597">
  <h2 class="product-title">
    <a>Al-Muwatta by Imam Malik</a>  <!-- English Title -->
  </h2>
  <div class="product-subtitle">الموطأ للإمام مالك</div>  <!-- Arabic Title -->
</div>
```

## Troubleshooting

**"403 Forbidden" or "Cloudflare Challenge"**
- The website is blocking automated access
- Try the workarounds listed above

**"No books found"**
- The URL might be incorrect
- The scholar might not have books listed on the website
- Check the debug HTML files created in the workspace

**Timeout errors**
- The website might be slow or down
- Try increasing timeout values in the code
- Check your internet connection

## Legal and Ethical Considerations

- **Respect robots.txt**: Check the website's robots.txt file
- **Rate limiting**: If you find a way to scrape, add delays between requests
- **Terms of Service**: Review the website's terms before scraping
- **Academic use**: If this is for research, contact the website for permission
- **Alternative**: Consider supporting the website by purchasing books or asking for data access

## Contributing

If you find a working solution to bypass Cloudflare or get permission from the website, please update the scrapers accordingly.

## License

This is a research/educational tool. Use responsibly and ethically.
