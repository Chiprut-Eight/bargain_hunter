from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def test_merkava_images_row():
    options = Options()
    options.add_argument('--headless=new')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    url = "https://merkava.mrp.gov.il/carpub/index.html"
    print(f"Loading {url}...")
    driver.get(url)
    
    try:
        # Wait for data table to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'panel') or contains(@class, 'card') or contains(text(), 'מכרז')]"))
        )
        time.sleep(5)
        
        # Click on the first div that looks like a row or card
        items = driver.find_elements(By.XPATH, "//*[contains(text(), 'מכרז מקוון')]")
        if not items:
            items = driver.find_elements(By.XPATH, "//tr")
            
        print(f"Found {len(items)} items. Clicking the first one...")
        if items:
             driver.execute_script("arguments[0].click();", items[0])
             time.sleep(5)
             
             images = driver.find_elements(By.TAG_NAME, "img")
             img_urls = [img.get_attribute("src") for img in images if img.get_attribute("src") and "base64" not in img.get_attribute("src")]
             print(f"URLs found after click: {img_urls}")
             
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    test_merkava_images_row()
