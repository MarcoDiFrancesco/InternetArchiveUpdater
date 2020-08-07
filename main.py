from selenium import webdriver
import socket
import os


def main():
    if socket.gethostname() == "bump":
        CHROMEDRIVER_PATH = "/home/marco/Downloads/chromedriver"
        GOOGLE_CHROME_BIN = "/usr/bin/google-chrome-stable"
    else:
        CHROMEDRIVER_PATH = os.environ.get("CHROMEDRIVER_PATH")
        GOOGLE_CHROME_BIN = os.environ.get("GOOGLE_CHROME_BIN")

    opts = webdriver.ChromeOptions()
    opts.binary_location = GOOGLE_CHROME_BIN
    opts.add_argument("--headless")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=opts)

    # Save page URL
    driver.get("http://web.archive.org/save")
    print("Web page opened")
    # Input text for new URL
    text_area = driver.find_element_by_id("web-save-url-input")
    text_area.send_keys("https://marcodifrancesco.com/")
    # Save page button
    save_button = driver.find_elements_by_class_name("web-save-button")
    # Click save button
    save_button[0].click()
    print("Save page button clicked")
    driver.close()
