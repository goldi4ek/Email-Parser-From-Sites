from logging import log
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import re
import os
from dotenv import load_dotenv
import time


class Scraper:
    """
    A class for scraping web pages and extracting email addresses and Facebook links.

    Attributes:
        driver (WebDriver): The Selenium WebDriver used for interacting with the web pages.

    Methods:
        __init__(self): Initializes the Scraper object and sets up the WebDriver.
        check_page(self, url): Checks the given page for email addresses and Facebook links.
        check_facebook_link(self, url): Checks if the given URL is a valid Facebook link.
        create_and_check_fb_link(self, url): Creates a Facebook link based on the given URL and processes the Facebook page.
        create_fb_link(self, url): Creates a Facebook link based on the given URL.
        find_email(self, page): Finds and returns the email address from the given page.
        find_facebook_link(self, page): Finds the Facebook link on a given page.
        process_facebook_page(self, facebook_link): Processes the Facebook page and extracts the email address from the contact information.
        close(self): Closes the web driver and releases any associated resources.
    """

    def __init__(self):
        load_dotenv()

        options = Options()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("--headless")
        service = Service("chromedriver.exe")
        self.driver = Chrome(service=service, options=options)

        self.login_to_facebook()

    def login_to_facebook(self):
        """
        Logs in to Facebook using the provided credentials.

        Returns:
            None
        """

        password = os.getenv("PASSWORD")
        phone_number = os.getenv("PHONE_NUMBER")

        self.driver.get("https://www.facebook.com/")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        email_input = self.driver.find_element(By.ID, "email")
        email_input.send_keys(phone_number)
        password_input = self.driver.find_element(By.ID, "pass")
        password_input.send_keys(password)
        login_button = self.driver.find_element(By.NAME, "login")
        login_button.click()

    def check_page(self, url):
        """
        Check the given page for email and Facebook link.

        Args:
            url (str): The URL of the page to check.

        Returns:
            str or None: The email found on the page, or None if no email or Facebook link is found.
        """
        print(f"\nChecking page: {url}:")
        try:
            response = requests.get(f"https://{url}", timeout=5)

            if not response.status_code == 200:
                return self.create_and_check_fb_link(url)

            page = BeautifulSoup(response.content, "html.parser")
            email = self.find_email(page)

            if email:
                print(email)
                return email

            facebook_link = self.find_facebook_link(page)

            if facebook_link:
                return self.process_facebook_page(facebook_link)

            return self.create_and_check_fb_link(url)

        except:
            try:
                return self.create_and_check_fb_link(url)

            except requests.exceptions.Timeout:
                print(f"Connection timed out for page: {url}")
                return None
            except requests.exceptions.SSLError:
                print(f"SSL error for page: {url}")
                return None
            except Exception as e:
                with open("log.txt", "a") as f:
                    f.write(f"Could not connect to {url}: {e}\n")
                print(f"Some error on page: {url}")
                return None

    def check_facebook_link(self, url):
        """
        Checks if the given URL is a valid Facebook link.

        Args:
            url (str): The URL to be checked.

        Returns:
            bool: True if the URL is a valid Facebook link, False otherwise.
        """
        facebook_link = url.split("/")
        return facebook_link[3] != "sharer" and facebook_link[3] != "dialog"

    def create_and_check_fb_link(self, url):
        """
        Creates a Facebook link based on the given URL and processes the Facebook page.

        Args:
            url (str): The URL to create the Facebook link from.

        Returns:
            str: Email address found on the Facebook page, or None if no email is found.
        """
        fb_link = self.create_fb_link(url)
        return self.process_facebook_page(fb_link)

    def create_fb_link(self, url):
        """
        Creates a Facebook link based on the given URL.

        Args:
            url (str): The URL of the website.

        Returns:
            str: The Facebook link.

        """
        name_of_fb_page = url.split(".")[0]
        return f"https://www.facebook.com/{name_of_fb_page}"

    def find_email(self, page):
        """
        Finds and returns the email address from the given page.

        Args:
            page (BeautifulSoup): The BeautifulSoup object representing the page.

        Returns:
            str or None: The email address found in the page, or None if no email address is found.
        """
        email = page.find(
            "a", href=re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
        )

        if email:
            return email["href"].split(":")[1]
        return None

    def find_facebook_link(self, page):
        """
        Finds the Facebook link on a given page.

        Args:
            page (BeautifulSoup): The BeautifulSoup object representing the page.

        Returns:
            str or None: The Facebook link if found, None otherwise.
        """
        facebook_pages = page.find_all("a", href=re.compile(r"facebook\.com"))

        for facebook_page in facebook_pages:
            if self.check_facebook_link(facebook_page["href"]):
                return facebook_page["href"]

        return None

    def process_facebook_page(self, facebook_link):
        print(facebook_link)
        """
        Process the Facebook page and extract the email address from the contact information.

        Args:
            facebook_link (str): The link to the Facebook page.

        Returns:
            str or None: The extracted email address if found, None otherwise.
        """
        self.driver.get(facebook_link)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        try:
            close_button = self.driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]",
            )
            close_button.click()
        except:
            pass

        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        info_block = soup.find(class_="x78zum5 x1n2onr6 xh8yej3")

        if not info_block:
            print(
                "No contact information found on Facebook page or page is not accessible"
            )
            return None

        for div in info_block.find_all("div"):
            if re.match(
                r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
                div.text,
            ):
                print(div.text)
                return div.text
        print("No email found on Facebook page")
        return None

    def close(self):
        """
        Closes the web driver and releases any associated resources.
        """
        self.driver.quit()
