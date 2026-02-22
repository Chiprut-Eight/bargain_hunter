"""
Find the correct API Topic/OfficeId for Tax Authority, Official Receiver, etc.
We use the Selenium JS fetch trick to call the Gov.il generic search and see what params work.
"""
import time, json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def get_driver():
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

def js_fetch(driver, url):
    js = f"var cb=arguments[0];fetch('{url}').then(r=>r.json()).then(d=>cb(d)).catch(e=>cb({{error:e.message}}));"
    return driver.execute_async_script(js)

if __name__ == "__main__":
    driver = get_driver()
    driver.get("https://www.gov.il/he/departments/publications/")
    time.sleep(5)

    print("=== Searching for ALL active publications (no filter) ===")
    r = js_fetch(driver, "https://www.gov.il/he/api/PublicationApi/Index?Skip=0&Limit=3")
    print(f"Total: {r.get('total')}, Page results: {len(r.get('results', []))}")
    for item in r.get('results', [])[:3]:
        print(f"  Title: {item.get('Title')}")
        print(f"  OfficeId: {item.get('OfficeId')}")
        print(f"  Topic: {item.get('Topic')}")
        print()

    # Try to find call_for_bids type
    print("\n=== Searching for 'call_for_bids' type ===")
    r2 = js_fetch(driver, "https://www.gov.il/he/api/PublicationApi/Index?Skip=0&Limit=10&PublicationType=call_for_bids")
    print(f"Total call_for_bids: {r2.get('total')}")
    for item in r2.get('results', [])[:5]:
        print(f"  [{item.get('PubDate', '')[:10]}] {item.get('Title')[:60]}")

    # Try broad search for customs (מכס)
    print("\n=== Searching with keyword 'מכס' ===")
    r3 = js_fetch(driver, "https://www.gov.il/he/api/PublicationApi/Index?Skip=0&Limit=5&Query=%D7%9E%D7%9B%D7%A1")
    print(f"Total 'מכס': {r3.get('total')}")
    for item in r3.get('results', [])[:5]:
        print(f"  [{item.get('PubDate', '')[:10]}] {item.get('Title')[:60]}")
        print(f"  OfficeId: {item.get('OfficeId')}, Url: {item.get('Url', '')[:50]}")

    # Official Receiver - try broader search
    print("\n=== Searching for 'כונס' ===")
    r4 = js_fetch(driver, "https://www.gov.il/he/api/PublicationApi/Index?Skip=0&Limit=5&Query=%D7%9B%D7%95%D7%A0%D7%A1")
    print(f"Total 'כונס': {r4.get('total')}")
    for item in r4.get('results', [])[:5]:
        print(f"  [{item.get('PubDate', '')[:10]}] {item.get('Title')[:60]}")
        print(f"  OfficeId: {item.get('OfficeId')}")

    driver.quit()
