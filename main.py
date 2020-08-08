from selenium import webdriver
import socket
import os


def read_file(file_name):
    with open(file_name, "r") as file:
        links = file.readlines()
    # Remove new lines with rstrip()
    return [link.rstrip() for link in links]


def main():
    opts = webdriver.ChromeOptions()

    # Set hostname for local debugging
    if socket.gethostname() == "bump":
        CHROME_DRIVER_PATH = "chromedriver"
        opts.binary_location = "/usr/bin/chromium"
    else:
        CHROME_DRIVER_PATH = os.environ.get("CHROME_DRIVER_PATH")
        opts.binary_location = os.environ.get("CHROME_PATH")
        opts.add_argument("--headless")

    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=opts)

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
