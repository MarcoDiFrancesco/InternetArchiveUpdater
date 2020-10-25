import os
import shutil
import socket
import time
from urllib.parse import urlparse
from driver import init_driver
from bs4 import BeautifulSoup


def delete_files_in_dir(folder):
    if not os.path.exists(folder):
        return
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print("Failed to delete %s. Reason: %s" % (file_path, e))


def same_domain(link):
    """
    Check if domain from given link and main link are equals
    e.g. from https://github.com/MarcoDiFrancesco
    github.com is taken and checked
    """
    if link.startswith("/"):
        return True
    main_domain = urlparse(URL).netloc  # e.g. github.com
    domain = urlparse(link).netloc
    if main_domain != domain:
        return False
    return True


def link_is_valid(link):
    if link.startswith("#"):
        return False
    if not same_domain(link):
        return False
    # Link is empty
    if not link:
        return False
    """
    From link: https://github.com/MarcoDiFrancesco/Gigi?hello=yes
    is taken: /MarcoDiFrancesco
    """
    link = urlparse(link).path
    """
    From URL: https://github.com/MarcoDiFrancesco
    if link does not start with: /MarcoDiFrancesco then
    discard it.

    From URL: https://github.com/ then accept it (because
    it's only a '/').
    """
    main_link = urlparse(URL).path
    if not link.startswith(main_link):
        return False
    return True


def get_links(url):
    """
    If does not contain domain name, add it.
    """
    if url.startswith("/"):
        main_url = urlparse(URL)
        url = f"{main_url.scheme}://{main_url.netloc}{url}"
    # Get selenium driver
    driver.get(url)
    page = driver.page_source
    soup = BeautifulSoup(page)
    global visited
    visited += 1

    for link in soup.findAll("a"):
        try:
            link = link["href"]
        except KeyError:
            pass
        else:
            if link_is_valid(link):
                # Keep only /MarcoDiFrancesco/Gigi
                link = urlparse(link).path
                # Reject duplicates
                if link not in links:
                    links.append(link)
        download_dir = os.environ.get("DOWNLOAD_DIR")
        delete_files_in_dir(download_dir)
        # Every 10 operations
    if visited % 10 == 0:
        export_list()


def export_list():
    export_path = os.environ.get("EXPORT_PATH")
    with open(export_path, "w") as f:
        f.write(f"{visited}/{len(links)}\n")
        for link in links:
            main_url = urlparse(URL)
            f.write(f"{main_url.scheme}://{main_url.netloc}{link}\n")


def import_list():
    export_path = os.environ.get("EXPORT_PATH")
    if not os.path.exists(export_path):
        return False
    with open(export_path, "r") as f:
        global visited, links
        visited = f.readline()
        # From 30/216 get 30
        visited = int(visited.split("/")[0])
        links = f.readlines()
        links = [line.replace("\n", "") for line in links]
        links = [urlparse(line).path for line in links]
    return True


def save_link(driver, url):
    """
    Save link into archive.org
    """
    if url.startswith("/"):
        main_url = urlparse(URL)
        url = f"{main_url.scheme}://{main_url.netloc}{url}"
    driver.get(f"http://web.archive.org/save/{url}")


def main():
    url = os.environ.get("URL")
    urls = []
    visited = 0

    driver = init_driver()
    if not import_list():
        get_links(URL)
    # While all urls are not visited
    while visited != len(urls):
        link = urls[visited]
        # Start timer
        t0 = time.time()
        get_links(link)
        save_link(driver, link)
        print(f"{visited}/{len(urls)}", link)
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
