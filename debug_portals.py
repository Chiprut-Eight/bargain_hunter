import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def debug_portals():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    print("--- ECA ---")
    driver.get("https://merkava.mrp.gov.il/rechev")
    time.sleep(10)
    print(driver.page_source[:2000])
    
    print("\n--- GOV IL ---")
    driver.get("https://www.gov.il/he/pages/real_estate_list")
    time.sleep(5)
    print(driver.page_source[:2000])
    
    driver.quit()

debug_portals()
