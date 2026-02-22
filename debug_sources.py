import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def test_url(url, name):
    print(f"\n--- Testing {name} ---")
    print(f"URL: {url}")
    try:
        # First try simple requests
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        res = requests.get(url, headers=headers, timeout=10)
        print(f"Requests Status: {res.status_code}")
        
        # Then try headless selenium to see if it renders more
        options = Options()
        options.add_argument('--headless=new')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)
        time.sleep(3) # allow render
        
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Look for typical auction/tender keywords
        keywords = ['מכרז', 'פומבי', 'הצעה', 'תאריך סגירה', 'pdf', 'קובץ']
        found = {k: page_source.count(k) for k in keywords if k in page_source}
        
        print(f"Keywords found in DOM: {found}")
        
        # Count links
        links = soup.find_all('a')
        print(f"Total links on page: {len(links)}")
        
        driver.quit()
    except Exception as e:
        print(f"Error testing {name}: {e}")

if __name__ == "__main__":
    urls = {
        "Tax Authority (Customs)": "https://www.gov.il/he/departments/publications/Call_for_bids/customs-auctions",
        "Official Receiver (Justice)": "https://www.gov.il/he/departments/publications/?OfficeId=b723f1dd-b541-4cfd-82d2-c48c9bef4187&Skip=0&Limit=10",
        "Tel Aviv Municipality": "https://www.tel-aviv.gov.il/Tenders/Pages/Tenders.aspx",
        "Sibet (MOD)": "https://www.mod.gov.il/Defence-and-Security/sibat/Pages/default.aspx"
    }
    
    for name, url in urls.items():
        test_url(url, name)
