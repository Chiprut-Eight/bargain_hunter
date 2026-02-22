"""
Find current working URL for Merkava ECA (hotzaa lapoal) auctions.
"""
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

options = Options()
options.add_argument('--headless=new')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
options.add_argument("window-size=1920,1080")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

urls_to_test = [
    "https://merkava.mrp.gov.il/",
    "https://merkava.mrp.gov.il/rechev/index.html",
    "https://eca.gov.il/",
    "https://www.gov.il/he/departments/ministry_of_justice/govil-landing-page",
    "https://www.moital.gov.il/NR/exeres/AF8A7E9B-D8B5-4D8E-89E3-F5DB69E21BFE.htm",
    "https://www.execution.justice.gov.il/",
]

for url in urls_to_test:
    try:
        driver.get(url)
        time.sleep(4)
        title = driver.title
        final_url = driver.current_url
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        links = [a.get('href','') for a in soup.find_all('a', href=True)][:5]
        print(f"\nURL: {url}")
        print(f"  Title: {title}")
        print(f"  Final URL: {final_url}")
        print(f"  Status: {'404/error' if 'שגיאה' in title or 'not found' in title.lower() else 'OK'}")
        if links:
            print(f"  Sample links: {links[:3]}")
    except Exception as e:
        print(f"\nURL: {url}\n  Error: {e}")

driver.quit()
