import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920,1080")

try:
    print("Launching browser...")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://apps.land.gov.il/MichrazimSite/")
    time.sleep(5)
    
    # 1. Click active tenders
    print("Clicking active tenders...")
    cards = driver.find_elements(By.CSS_SELECTOR, ".card")
    for card in cards:
        if "מכרזי מקרקעין פעילים" in card.text:
            btn = card.find_element(By.CSS_SELECTOR, "button")
            btn.click()
            break
            
    # 2. Wait for search page
    time.sleep(5)
    
    # 3. Click the 'Search' (חפש) button to load all active
    print("Clicking search button...")
    search_btns = driver.find_elements(By.XPATH, "//button[contains(text(), 'חפש')]")
    for btn in search_btns:
        try:
            btn.click()
            break
        except:
            pass
            
    print("Waiting 10s for results...")
    time.sleep(10)
    
    with open("ila_source3.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print("Saved source to ila_source3.html")
except Exception as e:
    print("Error:", e)
finally:
    driver.quit()
