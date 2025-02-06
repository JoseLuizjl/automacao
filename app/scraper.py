from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def download_images_from_url(url):
    service = Service()
    options = webdriver.EdgeOptions()
    options.add_argument('--headless')
    driver = webdriver.Edge(service=service, options=options)

    driver.get(url)     

    image_selectors = ['img', '.thumbnail', 'image']
    images_urls = []

    scroll_pause_time = 1  
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        for selector in image_selectors:
            try:
                images_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for img in images_elements:
                    img_url = img.get_attribute('src') or img.get_attribute('data-src') 
                    if img_url and img_url not in images_urls:  
                        images_urls.append(img_url)
                        print(f"Image found: {img_url}")  
                if len(images_urls) >= 40:  
                    break
            except Exception as e:
                print(f"Error finding images with selector {selector}: {e}")

        if len(images_urls) >= 40:
            break

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:  
            break
        last_height = new_height

    driver.quit()
    return images_urls
