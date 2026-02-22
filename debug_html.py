import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def dump_html(url, out_file):
    print(f"Loading {url} -> {out_file}")
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)
        time.sleep(5)
        
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("Done.")
    except Exception as e:
        print(e)
    finally:
        driver.quit()

if __name__ == "__main__":
    dump_html("https://www.gov.il/he/departments/publications/Call_for_bids/customs-auctions", "tax_auth.html")
    dump_html("https://www.gov.il/he/departments/publications/?OfficeId=b723f1dd-b541-4cfd-82d2-c48c9bef4187", "receiver.html")
    dump_html("https://www.mod.gov.il/Defence-and-Security/sibat/Pages/default.aspx", "sibet.html")
