import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def test_merkava_carpub():
    url = "https://merkava.mrp.gov.il/carpub/index.html"
    logging.info(f"Testing Selenium connection to {url}")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = None
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        driver.get(url)
        logging.info("Waiting for page to load...")
        time.sleep(10) # Give it plenty of time for any Angular/React to boot
        
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        
        print(f"Page Title: {soup.title.string if soup.title else 'No Title'}")
        
        # Save a snippet of the body to understand the DOM
        body_text = soup.body.text if soup.body else ""
        lines = [line.strip() for line in body_text.split('\n') if line.strip()]
        print("Body text snippet (first 100 lines):")
        for line in lines[:100]:
            print(line)
            
    except Exception as e:
        logging.error(f"Error: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    test_merkava_carpub()
