from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def test_gov_il():
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    url = "https://www.gov.il/he/departments/publications/Call_for_bids/customs-auctions"
    print(f"Loading {url}...")
    try:
        driver.get(url)
        time.sleep(5)
        
        page_source = driver.page_source
        
        if "Request unsuccessful" in page_source or "Incapsula" in page_source:
             print("Bot protection (Incapsula/Imperva) triggered.")
        else:
             print("Page loaded successfully without obvious bot block.")
             print(f"Number of links: {page_source.count('<a ')}")
             print(f"Title: {driver.title}")
             
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    test_gov_il()
