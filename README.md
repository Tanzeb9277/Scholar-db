# Islamic Scholars Book Database

This project aims to create a database of Islamic scholars and the books they have written by scraping book information from [sifatusafwa.com](https://www.sifatusafwa.com).

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   python3 -m playwright install chromium
   ```

2. **Edit your scholars list** in `scholars.json`

3. **Run the scraper:**
   ```bash
   python3 scraper_playwright.py
   ```

4. **View results** in `books_output.json`

## ⚠️ Important Note

The target website uses **Cloudflare anti-bot protection** which makes automated scraping challenging. The scrapers in this repository will run but may not retrieve data due to Cloudflare's challenge page.

**See `USAGE.md` for detailed instructions, workarounds, and alternative approaches.**

## Project Structure

```
.
├── README.md                   # This file
├── USAGE.md                    # Detailed usage instructions and troubleshooting
├── scholars.json               # Input: List of scholars (EDIT THIS)
├── scraper.py                  # Basic scraper (requests + BeautifulSoup)
├── scraper_playwright.py       # Advanced scraper (Playwright)
├── requirements.txt            # Python dependencies
└── books_output.json           # Output: Scraped book data
```

## Data Format

### Input (`scholars.json`)
```json
[
  {
    "name": "imam-malik",
    "hijri_year": "179"
  }
]
```

### Output (`books_output.json`)
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

## Need Help?

- **Cloudflare blocking the scraper?** → See workarounds in `USAGE.md`
- **Want to add more scholars?** → Edit `scholars.json` 
- **Different website?** → Modify the selectors in the scraper files

## Legal & Ethical

Please respect the website's terms of service and robots.txt. Consider reaching out to the website administrators for permission if you plan to scrape large amounts of data.
