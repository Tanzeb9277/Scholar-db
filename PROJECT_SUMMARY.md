# Islamic Scholars Books Database - Project Summary

## What Was Created

I've built a complete web scraping solution to extract book titles (English & Arabic) from sifatusafwa.com for Islamic scholars.

### 📁 Files Created

1. **`scraper_undetected.py`** ⭐ **RECOMMENDED**
   - Uses undetected-chromedriver to bypass Cloudflare
   - Best success rate
   - Opens a visible browser window
   - Waits for Cloudflare challenges automatically

2. **`scraper_playwright.py`**
   - Uses Playwright browser automation
   - Alternative to undetected-chromedriver
   - Can run headless

3. **`scraper.py`**
   - Basic scraper using requests + BeautifulSoup
   - Likely won't work due to Cloudflare
   - Included for reference

4. **`test_url.py`**
   - Helper tool to test scholar URLs
   - Usage: `python3 test_url.py imam-malik 179`
   - Generates JSON snippets for scholars.json

5. **`scholars.json`**
   - Input file - list of scholars to scrape
   - Already has one example (Imam Malik)
   - You need to add more scholars here

6. **`scholars_books.json`**
   - Output file - scraped results
   - JSON format with English & Arabic titles

7. **`README.md`**
   - Complete documentation
   - Troubleshooting guide
   - Legal/ethical considerations

8. **`USAGE.md`**
   - Step-by-step instructions
   - Quick start guide
   - Common issues and solutions

9. **`requirements.txt`**
   - All Python dependencies

## 🚀 How to Get Started

### Quick Start (3 steps)

```bash
# 1. Install dependencies
pip install -r requirements.txt
pip install undetected-chromedriver selenium

# 2. Add your scholars to scholars.json

# 3. Run the scraper
python3 scraper_undetected.py
```

### What Each Scholar Entry Needs

```json
{
  "name": "Display Name",
  "url_name": "url-slug-from-website",
  "death_year": "hijri-year"
}
```

**Example:** For https://www.sifatusafwa.com/en/manufacturer/imam-malik-179h.html

```json
{
  "name": "Imam Malik",
  "url_name": "imam-malik",
  "death_year": "179"
}
```

## ⚠️ Important: Cloudflare Protection

The website uses Cloudflare anti-bot protection. This means:

- **Basic HTTP requests are blocked** (403 Forbidden)
- **Browser automation is detected** and challenged
- **Undetected-chromedriver has the best success rate** (bypasses most checks)

### What Happens

1. The scraper opens a Chrome browser
2. Navigates to each scholar's page
3. Cloudflare shows "Verifying you are human..." (5-10 seconds)
4. Once verified, the page loads
5. Books are extracted and saved

## 📊 Output Format

```json
{
  "Imam Malik": {
    "death_year_hijri": "179",
    "url": "https://...",
    "books": [
      {
        "english_title": "Al-Muwatta by Imam Malik",
        "arabic_title": "الموطأ للإمام مالك"
      }
    ]
  }
}
```

## 🔧 Testing a URL

Before adding a scholar, test the URL:

```bash
python3 test_url.py imam-bukhari 256
```

This will:
- Test if the URL is accessible
- Check for Cloudflare protection
- Show you the JSON to add to scholars.json

## 📝 Adding More Scholars

### Method 1: Manual Discovery

1. Visit https://www.sifatusafwa.com/
2. Navigate to a scholar's page
3. Copy the URL
4. Extract the `url_name` and `death_year` from the URL
5. Add to `scholars.json`

### Method 2: Using the Test Tool

```bash
python3 test_url.py <url-name> <year>
```

It will generate the JSON entry for you.

## ✅ What to Expect

### Success Case
```
Scraping imam-malik (179H)...
URL: https://www.sifatusafwa.com/en/manufacturer/imam-malik-179h.html
  Waiting for page to load (Cloudflare may take 5-10 seconds)...
  Found 12 book(s)

✅ Scraping complete! Results saved to scholars_books.json
📚 Total scholars: 1
📖 Total books: 12
```

### Blocked Case
```
  Found 0 book(s)
```

**Solutions:**
1. Use `scraper_undetected.py` (best option)
2. Run during off-peak hours
3. Add longer delays
4. Try from a different network/IP

## 🛠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| "403 Forbidden" | Use `scraper_undetected.py` |
| "No books found" | Check URL is correct, or Cloudflare blocked |
| "Chrome not found" | Install Google Chrome or Chromium |
| "Module not found" | Run `pip install -r requirements.txt` |
| Cloudflare loop | Wait longer, try different IP |

## 📚 Example Scholars List

Here's a starter list (verify URLs first!):

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
  }
]
```

**⚠️ Warning:** These are examples. You MUST verify the actual URL format on the website!

## 🎯 Next Steps

1. **Populate `scholars.json`** with your list of scholars
2. **Test one scholar first** before running the full list
3. **Run `scraper_undetected.py`** for best results
4. **Check `scholars_books.json`** for the output
5. **Add more scholars** and repeat

## ⚖️ Legal & Ethical Notes

- This is for **educational/research purposes**
- Check the website's Terms of Service
- Respect robots.txt
- Add delays between requests (already built-in)
- Consider contacting the website for permission or API access
- If using for publication, cite the source

## 🤝 Support

- See `README.md` for full documentation
- See `USAGE.md` for detailed instructions
- Test URLs with `test_url.py`
- Check output in `scholars_books.json`

## 📖 Data Structure Extracted

For each book, the scraper extracts:
- **English Title**: From `<h2 class="product-title">`
- **Arabic Title**: From `<div class="product-subtitle">`

No other data (price, images, descriptions) is extracted.

## 🚦 Rate Limiting

Built-in delays:
- `scraper_undetected.py`: 3 seconds between scholars
- `scraper_playwright.py`: 2 seconds between scholars
- `scraper.py`: 1 second between scholars

You can adjust these in the code if needed.

---

## Summary

You now have a complete scraping solution with:
- ✅ 3 different scraping approaches
- ✅ URL testing tool
- ✅ Complete documentation
- ✅ Example data structure
- ✅ Cloudflare bypass attempt
- ✅ Error handling
- ✅ JSON output format

**Recommended workflow:**
1. Add 1-2 scholars to `scholars.json`
2. Run `python3 scraper_undetected.py`
3. Check results in `scholars_books.json`
4. Add more scholars
5. Repeat

Good luck building your Islamic Scholars database! 📚
