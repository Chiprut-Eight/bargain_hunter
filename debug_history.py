from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def test_merkava_history():
    options = Options()
    options.add_argument('--headless=new')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Try the main car pub index to look for a 'Results' or 'Closed' tab
    url = "https://merkava.mrp.gov.il/carpub/index.html"
    print(f"Loading {url}...")
    driver.get(url)
    
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//body"))
        )
        time.sleep(5)
        
        # Look for tabs or links that might say 'תוצאות', 'היסטוריה', 'סגורים'
        links = driver.find_elements(By.TAG_NAME, "a")
        buttons = driver.find_elements(By.TAG_NAME, "button")
        
        history_elements = []
        for el in links + buttons:
            text = el.text.strip()
            if "תוצאות" in text or "סגור" in text or "היסטורי" in text or "עבר" in text:
                history_elements.append(text)
                
        print(f"Found {len(history_elements)} potential history elements on main page.")
        if history_elements:
             print("Names:", history_elements)
        else:
             print("No obvious history/results tabs found on the current car portal.")
             
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    test_merkava_history()
