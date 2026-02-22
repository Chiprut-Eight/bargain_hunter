import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def dump_page_content(url, name):
    print(f"\n================ {name} ================")
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Print all list items or strong tags
        print("TENDERS / LIST ITEMS:")
        items = soup.find_all(['li', 'div'], class_=lambda c: c and ('item' in c.lower() or 'card' in c.lower() or 'list' in c.lower() or 'row' in c.lower()))
        for idx, item in enumerate(items[:10]):
            text = item.get_text(separator=' ', strip=True)
            if len(text) > 15:
                # print first 100 chars
                print(f"[{idx}] {text[:100]}")
                
        print("\nLINKS (first 20 containing text):")
        links = soup.find_all('a', href=True)
        count = 0
        for a in links:
            txt = a.get_text(strip=True)
            if txt and len(txt) > 3:
                print(f"- {txt} -> {a['href'][:50]}")
                count += 1
                if count >= 20:
                    break
                    
    except Exception as e:
        print(e)
    finally:
        driver.quit()

if __name__ == "__main__":
    dump_page_content("https://www.gov.il/he/departments/publications/Call_for_bids/customs-auctions", "Tax Authority")
    dump_page_content("https://www.gov.il/he/departments/publications/?OfficeId=b723f1dd-b541-4cfd-82d2-c48c9bef4187", "Official Receiver")
