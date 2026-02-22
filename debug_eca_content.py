"""
Quick debug: What does the ECA (Merkava rechev) page actually contain?
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

try:
    print("Loading ECA page...")
    driver.get("https://merkava.mrp.gov.il/rechev")
    time.sleep(12)  # Extra time for Angular

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    text = soup.get_text(separator='\n', strip=True)
    
    # Print everything
    lines = [l for l in text.split('\n') if len(l) > 10]
    print(f"\nTotal content lines: {len(lines)}")
    for i, l in enumerate(lines[:80]):
        print(f"[{i}] {l[:100]}")

    # Also check page title
    print(f"\nPage title: {driver.title}")
    print(f"URL: {driver.current_url}")

finally:
    driver.quit()
