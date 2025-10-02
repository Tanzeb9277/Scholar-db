# Quick Start Guide

## Step-by-Step Instructions

### 1. Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt

# For the undetected-chromedriver version (RECOMMENDED):
pip install undetected-chromedriver selenium
```

### 2. Populate Your Scholars List

Edit `scholars.json` with your list of scholars. I've included Imam Malik as an example.

**Finding the correct URL format:**

1. Go to https://www.sifatusafwa.com/
2. Search for a scholar or browse manufacturers
3. Find the URL pattern: `.../manufacturer/[name]-[year]h.html`
4. Extract the `[name]` and `[year]` parts

**Testing a URL:**

Use the included `test_url.py` helper:

```bash
python3 test_url.py imam-malik 179
```

This will test the URL and show you the JSON entry to add to `scholars.json`.

**Example:**
- URL: `https://www.sifatusafwa.com/en/manufacturer/imam-malik-179h.html`
- `url_name`: `"imam-malik"`
- `death_year`: `"179"`
- `name`: `"Imam Malik"` (display name)

Add to `scholars.json`:
```json
{
  "name": "Imam Malik",
  "url_name": "imam-malik",
  "death_year": "179"
}
```

### 3. Run the Scraper

**Option A: Try the Undetected ChromeDriver version (Best chance of success)**

```bash
python3 scraper_undetected.py
```

This will:
- Open a Chrome browser window
- Navigate to each scholar's page
- Wait for Cloudflare (10 seconds per page)
- Extract book titles
- Save to `scholars_books.json`

**Option B: Try the Playwright version**

```bash
playwright install chromium  # First time only
python3 scraper_playwright.py
```

**Option C: Try the basic requests version**

```bash
python3 scraper.py
```

### 4. View Results

The output is saved in `scholars_books.json`. You can view it in several ways:

**Option A: View in terminal (formatted)**
```bash
python3 view_results.py
```

**Option B: Export to CSV**
```bash
python3 view_results.py --csv
```
This creates `scholars_books.csv` for use in Excel/Google Sheets.

**Option C: Read the JSON directly**

The raw output in `scholars_books.json`:

```json
{
  "Imam Malik": {
    "death_year_hijri": "179",
    "url": "https://www.sifatusafwa.com/en/manufacturer/imam-malik-179h.html",
    "books": [
      {
        "english_title": "Al-Muwatta by Imam Malik",
        "arabic_title": "الموطأ للإمام مالك"
      },
      {
        "english_title": "Sharh Al-Muwatta",
        "arabic_title": "شرح الموطأ"
      }
    ]
  }
}
```

## Common Issues

### "Cloudflare Challenge" / No books found

The website uses Cloudflare protection. Solutions:

1. **Use `scraper_undetected.py`** - Has the best chance of bypassing Cloudflare
2. **Wait longer** - Cloudflare can take 5-10 seconds to verify
3. **Run in non-headless mode** - You can manually solve challenges if needed
4. **Try a different network** - Some IPs are flagged more than others

### "Module not found"

```bash
pip install -r requirements.txt
pip install undetected-chromedriver selenium
```

### "Chrome binary not found"

Make sure Google Chrome or Chromium is installed:

```bash
# Ubuntu/Debian
sudo apt install chromium-browser

# Or install Google Chrome from https://www.google.com/chrome/
```

## Tips for Success

1. **Start small** - Test with just one scholar first
2. **Add delays** - Don't hammer the server (code includes delays)
3. **Check URLs manually** - Verify URLs work in your browser first
4. **Be patient** - Cloudflare bypass can take time
5. **Run during off-peak hours** - Less likely to be rate-limited

## Finding More Scholars

To find scholars on sifatusafwa.com:

1. Visit: https://www.sifatusafwa.com/en/
2. Navigate to "Manufacturers" or use search
3. Click on a scholar
4. Copy the URL pattern
5. Add to `scholars.json`

## Example Scholars to Add

Here are some scholars you might want to add (verify URLs first):

```json
[
  {
    "name": "Imam Malik",
    "url_name": "imam-malik",
    "death_year": "179"
  },
  {
    "name": "Imam Ahmad",
    "url_name": "imam-ahmad-ibn-hanbal",
    "death_year": "241"
  },
  {
    "name": "Imam Bukhari",
    "url_name": "imam-bukhari",
    "death_year": "256"
  },
  {
    "name": "Imam Muslim",
    "url_name": "imam-muslim",
    "death_year": "261"
  }
]
```

**Note:** These are examples. You MUST verify the actual URLs on the website as the exact format may differ.

## Need Help?

1. Check the main README.md for more details
2. Look at the debug HTML files if created
3. Try running with visible browser (comment out headless mode)
4. Make sure you have permission to scrape the website
