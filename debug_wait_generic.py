import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def test_generic_api():
    print(f"\n--- Loading Generic API ---")
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    try:
        driver.get("https://www.gov.il/he/departments/publications/")
        time.sleep(5)
        
        # Fetch generic publications from page 1 to see if we get items
        api_url = "https://www.gov.il/he/api/PublicationApi/Index?Skip=0&Limit=5"
             
        js_code = f"""
        var callback = arguments[0];
        fetch('{api_url}')
          .then(r => r.json())
          .then(data => callback(data))
          .catch(e => callback({{"error": e.message}}));
        """
        result = driver.execute_async_script(js_code)
        if isinstance(result, dict) and "results" in result:
             print(f"Generic Results found: {len(result['results'])}")
             for i in result['results'][:3]:
                 print(f" - {i.get('Title')}")
        else:
             print(result)
    except Exception as e:
        print(e)
    finally:
        driver.quit()

if __name__ == "__main__":
    test_generic_api()
