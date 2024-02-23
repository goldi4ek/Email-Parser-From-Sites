from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import re


class Scraper:
    def __init__(self):
        options = Options()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("--headless")
        service = Service("chromedriver.exe")
        self.driver = Chrome(service=service, options=options)

    def check_page(self, url):
        print(f"\nChecking page: {url}:")
        try:
            response = requests.get(f"https://{url}", timeout=5)

            if response.status_code == 200:
                page = BeautifulSoup(response.content, "html.parser")
                email = self.find_email(page)

                if email:
                    print(email)
                    return email
                else:
                    facebook_link = self.find_facebook_link(page)

                    if facebook_link:
                        if self.check_facebook_link(facebook_link):
                            return self.process_facebook_page(facebook_link)
                        else:
                            try:
                                self.create_and_check_fb_link(url)
                            except:
                                print("Wrong facebook link format")
                                return None
                    else:
                        print("No email and facebook found")
                        return None
            else:
                self.create_and_check_fb_link(url)
                print(
                    f"Failed to load page: {url} with status code {response.status_code}"
                )
        except:
            try:
                self.create_and_check_fb_link(url)

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
        facebook_link = url.split("/")
        return len(facebook_link) == 4

    def create_and_check_fb_link(self, url):
        fb_link = self.create_fb_link(url)
        self.process_facebook_page(fb_link)

    def create_fb_link(self, url):
        name_of_fb_page = url.split(".")[0]
        return f"https://www.facebook.com/{name_of_fb_page}"

    def find_email(self, page):
        email = page.find("a", href=re.compile(r"mailto:"))

        if email:
            return email["href"].split(":")[1]
        return None

    def find_facebook_link(self, page):
        facebook_link = page.find("a", href=re.compile(r"facebook\.com"))

        if facebook_link:
            return facebook_link["href"]
        return None

    def process_facebook_page(self, facebook_link):
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

        if info_block:
            for div in info_block.find_all("div"):
                if re.match(
                    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
                    div.text,
                ):
                    print(div.text)
                    return div.text
            print("No email found on Facebook page")
            return None
        else:
            print("No contact information found on Facebook page")
            return None

    def close(self):
        self.driver.quit()