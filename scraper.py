import os
from driver import Driver
from db import PG
from urllib.parse import urlparse


def main():
    url = os.environ.get("MAIN_URL")
    driver = Driver()
    db = PG()
    while True:
        urls = db.get_urls()
        if not urls:
            urls = [driver.main_url]
        new_urls = set()
        for url in urls:
            print(url)
            new_urls = new_urls.union(driver.get_urls(url))
        db.insert_urls(new_urls)
        print("Status: ", db.get_status())


if __name__ == "__main__":
    main()
