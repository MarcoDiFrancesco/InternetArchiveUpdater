from selenium import webdriver
import os

CHROMEDRIVER_PATH = os.environ.get("CHROMEDRIVER_PATH")
GOOGLE_CHROME_BIN = os.environ.get("GOOGLE_CHROME_BIN")

opts = webdriver.ChromeOptions()
opts.binary_location = GOOGLE_CHROME_BIN
opts.add_argument("--headless")
opts.add_argument("--disable-dev-shm-usage")
opts.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=opts)

driver.get("https://www.google.com")
print(driver.page_source)
