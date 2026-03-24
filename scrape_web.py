import pandas as pd
import requests
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import time

# Get the Tax ID from the excel sheet

df = pd.read_excel(r"C:\Users\tc13g\Downloads\Master Association List.xlsx")

for index, row in df.head(10).iterrows():
    tax_id = str(row.iloc[4]).strip().replace("-", "")
    print(f"Checking row {index}, tax id = {tax_id}")

    url = "https://search.sunbiz.org/Inquiry/CorporationSearch/SearchResults"
    params = {
        "inquiryType": "FeiNumber",
        "searchTerm": tax_id
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"
    }

    query_string = urlencode(params)
    full_url = url + "?" + query_string

    request = Request(full_url, headers=headers)
    web_byte = urlopen(request).read()
    webpage = web_byte.decode('utf-8')

    soup = BeautifulSoup(webpage, "html.parser")

    for a in soup.find_all("a", href=True):
        text = a.get_text(strip=True)
        href = a["href"]

        if text == tax_id:
            detail_url = "https://search.sunbiz.org" + href

            second_request = Request(detail_url, headers=headers)
            second_web_byte = urlopen(second_request).read()
            second_webpage = second_web_byte.decode('utf-8')

            soup = BeautifulSoup(second_webpage, "html.parser")
            annual_reports_text = soup.find(string="Annual Reports")
            annual_reports_table = annual_reports_text.parent.find_next("table")
            
            if "2026" in annual_reports_table.get_text():
                df.at[index, "2026 Annual Report"] = "Yes"
            else:
                df.at[index, "2026 Annual Report"] = "No"
                
            break
    
    df.to_excel(r"C:\Users\tc13g\Downloads\Master Association List.xlsx", index=False)
    time.sleep(5)



