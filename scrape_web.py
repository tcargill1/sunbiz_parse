import pandas as pd
import requests
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from bs4 import BeautifulSoup

# Get the Tax ID from the excel sheet

df = pd.read_excel(r"C:\Users\tc13g\Downloads\Master Association List.xlsx")

for index, row in df.head(1).iterrows():
    tax_id = str(row.iloc[4]).strip().replace("-", "")
    print(f"Checking row {index}, tax id = {tax_id}")

    url = "https://search.sunbiz.org/Inquiry/CorporationSearch/SearchResults"
    params = {
        "inquiryType": "FeiNumber",
        "searchTerm": tax_id
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
        "accept": '"text/html,application...',
        "referer": 'https://...',
    }

    query_string = urlencode(params)
    full_url = url + "?" + query_string

    request = Request(full_url, headers=headers)
    web_byte = urlopen(request).read()
    webpage = web_byte.decode('utf-8')

    print(webpage)

