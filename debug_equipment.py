from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def explore_merkava_equipment():
    options = Options()
    options.add_argument('--headless=new')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Let's search mr.gov.il with a specific query for equipment / ECA
    print("Testing Merkava search for 'הוצאה לפועל'...")
    # The URL often accepts a 'q' parameter or we can just go to the URL and print the page source
    url = "https://mr.gov.il/ilgstorefront/he/search/?s=TENDER&q=%D7%94%D7%95%D7%A6%D7%90%D7%94+%D7%9C%D7%A4%D7%95%D7%A2%D7%9C"
    driver.get(url)
    time.sleep(8)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    results = soup.find_all('div', class_=lambda c: c and 'result-item-title' in c.lower())
    if not results:
         results = soup.find_all('a', class_=lambda c: c and 'title' in c.lower())
         
    print(f"Found {len(results)} potential elements matching הוצאה לפועל")
    
    for r in results[:5]:
        print(r.get_text(strip=True))
        print("Link:", r.get('href'))
        print("---")
        
    driver.quit()

if __name__ == "__main__":
    explore_merkava_equipment()
