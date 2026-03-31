import pandas as pd
import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import time
import random

# ── Sign up free at https://www.scraperapi.com → get your API key ────────────
SCRAPER_API_KEY = "eb4f188ee815ff43b6fd721a4fa7482c"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
]

def scraper_api_get(url, retries=3):
    """Route request through ScraperAPI which handles IP rotation automatically."""
    api_url = "https://api.scraperapi.com/"
    params = {
        "api_key": SCRAPER_API_KEY,
        "url": url,
        "render": "false"  # set to "true" if site uses JS rendering
    }
    headers = {"User-Agent": random.choice(USER_AGENTS)}

    for attempt in range(retries):
        try:
            resp = requests.get(api_url, params=params, headers=headers, timeout=60)
            if resp.status_code == 200:
                return resp.text
            elif resp.status_code == 403:
                print(f"  Attempt {attempt+1}: 403 Forbidden — retrying...")
            elif resp.status_code == 429:
                print(f"  Rate limited — waiting 30s...")
                time.sleep(30)
            else:
                print(f"  Attempt {attempt+1}: HTTP {resp.status_code}")
        except Exception as e:
            print(f"  Attempt {attempt+1} error: {e}")
        time.sleep(5 * (attempt + 1))  # backoff: 5s, 10s, 15s

    raise Exception(f"All {retries} attempts failed for {url}")


# ── Main ─────────────────────────────────────────────────────────────────────
print("=== Sunbiz 2026 Annual Report Checker ===")
print("Enter the full path to your Excel file.")
print(r"Example: C:\Users\yourname\Downloads\Master Association List.xlsx")
excel_path = input("File path: ").strip().strip('"')  # strip quotes in case they drag-and-drop

df = pd.read_excel(excel_path)

for index, row in df.iloc.iterrows():
    tax_id = str(row.iloc[4]).strip().replace("-", "")
    print(f"\nRow {index} | Tax ID: {tax_id}")

    params = {"inquiryType": "FeiNumber", "searchTerm": tax_id}
    search_url = "https://search.sunbiz.org/Inquiry/CorporationSearch/SearchResults?" + urlencode(params)

    try:
        webpage = scraper_api_get(search_url)
    except Exception as e:
        print(f"  SKIPPED (search failed): {e}")
        df.at[index, "2026 Annual Report"] = "Error"
        continue

    soup = BeautifulSoup(webpage, "html.parser")
    matched = False

    for a in soup.find_all("a", href=True):
        if a.get_text(strip=True) == tax_id:
            detail_url = "https://search.sunbiz.org" + a["href"]
            try:
                second_webpage = scraper_api_get(detail_url)
            except Exception as e:
                print(f"  SKIPPED (detail failed): {e}")
                df.at[index, "2026 Annual Report"] = "Error"
                matched = True
                break

            soup2 = BeautifulSoup(second_webpage, "html.parser")
            annual_reports_text = soup2.find(string="Annual Reports")
            if annual_reports_text:
                table = annual_reports_text.parent.find_next("table")
                df.at[index, "2026 Annual Report"] = "Yes" if "2026" in table.get_text() else "No"
                print(f"  → 2026 Annual Report: {df.at[index, '2026 Annual Report']}")
            else:
                df.at[index, "2026 Annual Report"] = "Not Found"
                print("Not found")
            matched = True
            break

    if not matched:
        df.at[index, "2026 Annual Report"] = "No Match"

    df.to_excel(excel_path, index=False)
    time.sleep(3 + 7 * random.random())  # 3–10s delay