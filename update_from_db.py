import os
import socket
import time
from urllib.parse import urlparse
from driver import Driver
from db import PG
from driver import Driver


def export_list():
    export_path = os.environ.get("EXPORT_PATH")
    with open(export_path, "w") as f:
        f.write(f"{visited}/{len(links)}\n")
        for link in links:
            main_url = urlparse(URL)
            f.write(f"{main_url.scheme}://{main_url.netloc}{link}\n")


# def import_list():
#     export_path = os.environ.get("EXPORT_PATH")
#     if not os.path.exists(export_path):
#         return False
#     with open(export_path, "r") as f:
#         global visited, links
#         visited = f.readline()
#         # From 30/216 get 30
#         visited = int(visited.split("/")[0])
#         links = f.readlines()
#         links = [line.replace("\n", "") for line in links]
#         links = [urlparse(line).path for line in links]
#     return True


def archive_url(driver, url):
    """
    Save link into archive.org
    """
    if url.startswith("/"):
        main_url = urlparse(URL)
        url = f"{main_url.scheme}://{main_url.netloc}{url}"
    driver.get(f"http://web.archive.org/save/{url}")


def get_urls(db):
    """
    Get n urls from database
    """
    print("Getting URLS")
    return db.fetchall("SELECT * FROM url;")


def main():
    driver = Driver()
    db = PG()

    while True:
        urls = get_urls(db)
        for conter, url in enumerate(urls):
            # Start timer
            t0 = time.time()
            archive_url(driver, url)
            print(f"{conter}/{len(urls)}", url)
            """
            Make 15 requests/minute.
            4.3 instead of 4 to make at most 14 requestes/minute.
            """
            # End timer
            t1 = time.time() - t0
            if t1 < 4.3:
                time.sleep(4.3 - t1)


if __name__ == "__main__":
    main()
