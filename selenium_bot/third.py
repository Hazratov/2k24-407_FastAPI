import time
import json
import psycopg2
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from faker import Faker
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# FIREFOX CONFIGURATION
gecko_path = "/snap/firefox/current/usr/lib/firefox/geckodriver"
firefox_path = "/snap/firefox/current/usr/lib/firefox/firefox"


fake = Faker()
fake_ru = Faker('ru_RU')
service = Service(gecko_path)
options = webdriver.FirefoxOptions()
options.add_argument("--window-size=1920x1080")
options.add_argument("--incognito")
options.binary_location = firefox_path

driver = webdriver.Firefox(service=service, options=options)
wait = WebDriverWait(driver, 30)

# Open site
driver.get("https://sales-inquiries.ae/axcapital/al-jazi/")

# Wait for popup to appear
popup = ('xpath', '//*[@id="popupModal"]/div/div/div')
wait.until(EC.visibility_of_element_located(popup))

print("Page title:", driver.title)

name = driver.find_element(By.XPATH,'//*[@id="popupModal"]/div/div/div/div[1]/form/div[1]/input')
email = driver.find_element(By.XPATH,'//*[@id="popupModal"]/div/div/div/div[1]/form/div[2]/input')
phone = driver.find_element(By.XPATH,'//*[@id="popupModal"]/div/div/div/div[1]/form/div[3]/div/input')
download_button = driver.find_element(By.XPATH,'//*[@id="popupModal"]/div/div/div/div[1]/form/button')
# ok_button = driver.find_element(By.XPATH,'/html/body/div[10]/div/div[6]/button[1]')

name.send_keys(fake.name())
email.send_keys(fake.email())
phone.send_keys(fake_ru.phone_number().replace('+', ''))
time.sleep(5)
driver.save_screenshot("form-screenshot.png")

print(phone)
time.sleep(5)
download_button.click()
# ok_button.click()
time.sleep(5)
driver.quit()