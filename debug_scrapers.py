import logging
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_tax_authority_data(driver):
    """
    Scrape Israel Tax Authority / Customs confiscated goods auctions.
    URL: https://www.gov.il/he/departments/publications/Call_for_bids/customs-auctions
    """
    logging.info("Starting Tax Authority (Customs) Scrape...")
    url = "https://www.gov.il/he/departments/publications/Call_for_bids/customs-auctions"
    deals = []
    
    try:
        driver.get(url)
        time.sleep(5)
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # In Gov.il call for bids, usually items are under a list or table.
        # Let's grab 'a' tags that look like auctions or pdfs
        links = soup.find_all('a', href=True)
        
        auction_links = []
        for a in links:
            text = a.get_text(strip=True)
            if "מכרז" in text or "מכירה" in text or "פומבית" in text or "קובץ" in text:
                 auction_links.append((text, a['href']))
                 
        for idx, (text, href) in enumerate(auction_links[:5]):
            if text and len(text) > 5 and not text.startswith("http"):
                deal = {
                    "id": f"tax_auth_{idx}",
                    "type": "equipment",
                    "title": f"מכס/רשות המסים: {text}",
                    "source": "רשות המסים - מכס",
                    "openingPrice": 0,
                    "marketValue": 0,
                    "timeLeft": "פרטים בקובץ",
                    "link": href if href.startswith("http") else f"https://www.gov.il{href}"
                }
                deals.append(deal)
                
        logging.info(f"Successfully scraped {len(deals)} items from Tax Authority.")
        
    except Exception as e:
        logging.error(f"Tax Authority scraping failed: {e}")
        
    return deals

def get_official_receiver_data(driver):
    """
    Scrape Official Receiver (Justice Ministry) properties/businesses.
    URL: https://www.gov.il/he/departments/publications/?OfficeId=b723f1dd-b541-4cfd-82d2-c48c9bef4187
    """
    logging.info("Starting Official Receiver (Ministry of Justice) Scrape...")
    url = "https://www.gov.il/he/departments/publications/?OfficeId=b723f1dd-b541-4cfd-82d2-c48c9bef4187"
    deals = []
    
    try:
        driver.get(url)
        time.sleep(5)
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Typically the results are in a list format
        items = soup.find_all('div', class_=lambda c: c and 'item' in c.lower())
        if not items:
            # Fallback to links
            items = soup.find_all('a', href=True)
            
        count = 0
        for item in items:
            text = item.get_text(strip=True)
            if "מכירת" in text or "הזמנה להציע" in text or "כינוס" in text:
                href = item['href'] if item.name == 'a' else item.find('a')['href'] if item.find('a') else url
                title = text.split('\n')[0][:100]
                
                # Try to guess type based on text
                dt = "real_estate" if "דירה" in text or "מקרקעין" in text or "נכס" in text else "equipment"
                
                deal = {
                    "id": f"justice_{count}",
                    "type": dt,
                    "title": f"כונס רשמי: {title}",
                    "source": "משרד המשפטים - כונס הנכסים הרשמי",
                    "openingPrice": 0,
                    "marketValue": 0,
                    "timeLeft": "פתוח להצעות",
                    "link": href if href.startswith("http") else f"https://www.gov.il{href}"
                }
                deals.append(deal)
                count += 1
                if count >= 3:
                    break
        
        logging.info(f"Successfully scraped {len(deals)} items from Official Receiver.")
        
    except Exception as e:
        logging.error(f"Official Receiver scraping failed: {e}")
        
    return deals

# Test script
if __name__ == "__main__":
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium import webdriver
    logging.basicConfig(level=logging.INFO)
    
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    res1 = get_tax_authority_data(driver)
    res2 = get_official_receiver_data(driver)
    
    for d in res1 + res2:
        print(d)
        
    driver.quit()
