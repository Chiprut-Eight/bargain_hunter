from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def explore_mr_gov_il():
    options = Options()
    options.add_argument('--headless=new')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    url = "https://mr.gov.il/ilgstorefront/he/search/?s=TENDER"
    print(f"Testing {url}...")
    driver.get(url)
    time.sleep(10)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # We want to specifically find the main cards for tenders
    # Often they are inside li or div with class 'list-item' or 'card'
    items = soup.find_all(lambda tag: tag.name in ['li', 'div'] and tag.get('class') and any('result' in c.lower() or 'item' in c.lower() for c in tag.get('class')))
    
    found_count = 0
    for i in items:
        text = i.get_text(strip=True)
        if len(text) > 30 and ("ציוד" in text or "מטלטלין" in text or "מכרז" in text):
             print(f"Snippet: {text[:150]}")
             link = i.find('a')
             if link:
                 print(f"Link: {link.get('href')}")
             print("---")
             found_count += 1
             if found_count > 5:
                 break
                 
    driver.quit()

if __name__ == "__main__":
    explore_mr_gov_il()
