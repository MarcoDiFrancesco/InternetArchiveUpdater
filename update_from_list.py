from selenium import webdriver
import socket
import os


def init_driver():
    opts = webdriver.ChromeOptions()

    chrome_driver_path = os.environ.get("CHROME_DRIVER_PATH")
    chrome_path = os.environ.get("CHROME_PATH")
    debug = os.environ.get("DEBUG")

    # Check if variables are sourced
    if not chrome_driver_path or not chrome_path:
        raise ValueError("Source variables before running program")

    opts.binary_location = chrome_path
    # Show window if dubug is on
    if not debug:
        opts.add_argument("--headless")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=chrome_driver_path, options=opts)
    return driver


def read_file(file_name):
    with open(file_name, "r") as file:
        links = file.readlines()
    # Remove new lines with rstrip()
    return [link.rstrip() for link in links]


def main():
    driver = init_driver()

    # Read URLs from file
    links = read_file("links.txt")

    for link in links:
        # Save page URL
        driver.get(f"http://web.archive.org/save/{link}")
        print(f"Page requested: {link}")

    # Close connection
    driver.close()


if __name__ == "__main__":
    # Used for testing
    main()
