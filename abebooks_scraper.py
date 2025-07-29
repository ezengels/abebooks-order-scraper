import pandas as pd
import selenium
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def nextpage():
    try:
        driver.find_element(By.LINK_TEXT, 'Next Page')
        return True
    except NoSuchElementException:
        return False

def scraper():
    dropdowns = driver.find_elements(By.CLASS_NAME, 'disclosure')
    for dropdown in dropdowns:
        dropdown.click()
    purchases = driver.find_elements(By.CLASS_NAME, 'panel-default')
    for purchase in purchases:
        p = str(purchase.text)
        data.append(p)
    dropdowns.clear()
    purchases.clear()

driver = webdriver.Firefox()
driver.get('https://www.abebooks.com/')
sopage = driver.find_element(By.ID, 'my-account')
sopage.click()

email = driver.find_element(By.ID, 'ap_email')
password = driver.find_element(By.ID, 'ap_password')
so = driver.find_element(By.ID, 'signInSubmit')

email.send_keys('USERNAME')
password.send_keys('PASSWORD')
so.click()

driver.find_element(By.PARTIAL_LINK_TEXT, 'View My Purchases').click()

data = []

while nextpage() == True:
    scraper()
    driver.find_element(By.LINK_TEXT, 'Next Page').click()
    if nextpage() == False:
        scraper()
        break

df = pd.DataFrame(data)
df.to_csv('abebooks_raw_purchase_data.csv', sep=',', encoding='utf-8', index=False, header=False)