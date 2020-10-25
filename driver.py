from selenium import webdriver
import os


def init_driver():
    opts = webdriver.ChromeOptions()

    chrome_driver_path = os.environ.get("CHROME_DRIVER_PATH")
    chrome_path = os.environ.get("CHROME_PATH")

    if not chrome_driver_path or not chrome_path:
        raise ValueError("Source variables before running program")

    opts.binary_location = chrome_path
    opts.add_argument("--headless")
    prefs = {
        "download.open_pdf_in_system_reader": False,
        "download.prompt_for_download": True,
        "download.default_directory": DOWNLOAD_DIR,
        "plugins.always_open_pdf_externally": False,
    }
    opts.add_experimental_option("prefs", prefs)
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=chrome_driver_path, options=opts)
    return driver
