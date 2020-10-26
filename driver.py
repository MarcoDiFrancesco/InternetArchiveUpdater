from selenium import webdriver
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import shutil
import time
from random import randint


class Driver:
    def __init__(self):
        self.get_envvars()

        opts = webdriver.ChromeOptions()
        opts.binary_location = self.chrome_path
        if not self.debug:
            opts.add_argument("--headless")
        prefs = {
            "download.open_pdf_in_system_reader": False,
            "download.prompt_for_download": True,
            "download.default_directory": self.download_dir,
            "plugins.always_open_pdf_externally": False,
        }
        opts.add_experimental_option("prefs", prefs)
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(
            executable_path=self.chrome_driver_path, options=opts
        )

    def get_envvars(self):
        self.chrome_driver_path = os.environ.get("CHROME_DRIVER_PATH")
        self.chrome_path = os.environ.get("CHROME_PATH")
        self.download_dir = os.environ.get("DOWNLOAD_DIR")
        self.main_url = os.environ.get("MAIN_URL")
        self.debug = os.environ.get("DEBUG")

    def get_page_soruce(self, url):
        """
        Get source of a given url's page
        """
        self.driver.get(url)
        return self.driver.page_source

    def get_urls(self, url):
        """
        Get list of all urls of a given url's page.

        If does not contain domain name, add it.
        e.g. if -> /MarcoDiFrancesco/Gigi
        make it -> https://github.com/MarcoDiFrancesco/Gigi
        """

        if url.startswith("/"):
            main_url = urlparse(self.main_url)
            url = f"{main_url.scheme}://{main_url.netloc}{url}"

        urls = set()
        page = self.get_page_soruce(url)
        soup = BeautifulSoup(page, features="html.parser")

        # Detect error
        if soup.find("h1", text="Whoa there!"):
            sec = randint(15, 30)
            print(f"Too many requests, waiting {sec}")
            time.sleep(sec)
        page_urls = soup.findAll("a")

        for url in page_urls:
            try:
                url = url["href"]
            except KeyError:
                pass
            else:
                if self.url_is_valid(url):
                    # Keep only /MarcoDiFrancesco/Gigi
                    url = urlparse(url).path
                    urls.add(url)
        self._delete_files_in_dir(self.download_dir)
        return urls

    def same_domain(self, url):
        """
        Check if domain from given url and main url are equal
        e.g. from https://github.com/MarcoDiFrancesco
        github.com is taken and checked
        """
        if url.startswith("/"):
            return True
        main_domain = urlparse(self.main_url).netloc  # e.g. github.com
        domain = urlparse(url).netloc
        if main_domain != domain:
            return False
        return True

    # def clean_url(self, url):
    #     if url.startswith("/"):
    #         main_url = urlparse(url)
    #         url = f"{main_url.scheme}://{main_url.netloc}{url}"
    #     return url

    def url_is_valid(self, url):
        if url.startswith("#"):
            return False
        if not self.same_domain(url):
            return False
        # url is empty
        if not url:
            return False
        """
        From url: https://github.com/MarcoDiFrancesco/Gigi?hello=yes
        is taken: /MarcoDiFrancesco
        """
        url = urlparse(url).path
        """
        From URL: https://github.com/MarcoDiFrancesco
        if url does not start with: /MarcoDiFrancesco then
        discard it.

        From URL: https://github.com/ then accept it (because
        it's only a '/').
        """
        main_domain = urlparse(self.main_url).path
        if not url.startswith(main_domain):
            return False
        return True

    def _delete_files_in_dir(self, dir):
        """
        Delete all files inside a given directory
        """
        if not os.path.exists(dir):
            return
        for filename in os.listdir(dir):
            file_path = os.path.join(dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print("Failed to delete %s. Reason: %s" % (file_path, e))
