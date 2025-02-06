import re
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import pandas as pd


service = Service()
options = webdriver.EdgeOptions()
options.add_argument('--headless')
driver = webdriver.Edge(service=service, options=options)


url = 'https://books.toscrape.com/'
driver.get(url)

titles = driver.find_elements(By.TAG_NAME, 'a')[54:94:2]

titleList = []
stockList = []

for i in range(len(titles)):
    titles = driver.find_elements(By.TAG_NAME, 'a')[54:94:2]
    titleList.append(titles[i].get_attribute('title'))

    titles[i].click()  
    
    try:
        getStock = driver.find_element(By.CSS_SELECTOR, 'p.instock.availability').text.strip()
        match = re.search(r'\((\d+)\s+available\)', getStock)

        if match:
            stockList.append(match.group(1))  
        else:
            stockList.append("N/A")
    except Exception as e:
        print(f'Error: {e}')
        stockList.append("Error")
    
    driver.back()  

dictDF = {'title': titleList, 'stock': stockList}
df = pd.DataFrame(dictDF)
df.to_csv('BookInfo.csv', sep=',', index=False, encoding='utf-8')

input("\nPress Enter to close the browser ...")
driver.quit()
