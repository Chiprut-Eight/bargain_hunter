import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json

def get_rendered_data(url, name):
    print(f"\n--- Loading {name} ---")
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    try:
        driver.get(url)
        print("Waiting 10 seconds for Angular to load data...")
        time.sleep(10)
        
        # We can also check window.state or fetch from API using the driver's cookies
        # Let's execute a JS fetch to the API since we have the cookies now
        api_url = "https://www.gov.il/he/api/PublicationApi/Index?Skip=0&Limit=10"
        if "customs" in url:
             api_url += "&Topic=customs-auctions"
        else:
             api_url += "&OfficeId=b723f1dd-b541-4cfd-82d2-c48c9bef4187"
             
        js_code = f"""
        var callback = arguments[0];
        fetch('{api_url}')
          .then(r => r.json())
          .then(data => callback(data))
          .catch(e => callback({{"error": e.message}}));
        """
        print("Executing JS Fetch to API...")
        result = driver.execute_async_script(js_code)
        
        with open(f"{name}_data.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
            
        print(f"Data saved. Keys: {result.keys() if isinstance(result, dict) else type(result)}")
        
        if isinstance(result, dict) and "results" in result:
             print(f"Results list size: {len(result['results'])}")
             for i in result['results'][:2]:
                 print(f" - {i.get('Title')}")
        
    except Exception as e:
        print(e)
    finally:
        driver.quit()

if __name__ == "__main__":
    get_rendered_data("https://www.gov.il/he/departments/publications/Call_for_bids/customs-auctions", "tax_auth")
    get_rendered_data("https://www.gov.il/he/departments/publications/?OfficeId=b723f1dd-b541-4cfd-82d2-c48c9bef4187", "receiver")
