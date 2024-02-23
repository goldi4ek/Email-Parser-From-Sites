from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup
import re


class Scraper:
    def __init__(self):
        # Set up the Chrome driver
        options = Options()
        options.add_argument("--headless")
        service = Service("chromedriver.exe")
        self.driver = Chrome(service=service)

    # Check the page for an email address
    def check_page(self, url):
        response = requests.get(f"https://{url}")
        page = BeautifulSoup(response.content, "html.parser")
        email = self.find_email(page)
        if email:
            print(email)
        else:
            facebook_link = self.find_facebook_link(page)
            if facebook_link:
                self.process_facebook_page(facebook_link)
            else:
                print("No email and facebook found")

    # Find the email address on the page
    def find_email(self, page):
        email = page.find("a", href=re.compile(r"mailto:"))
        if email:
            return email["href"].split(":")[1]
        return None

    # Find the Facebook link on the page
    def find_facebook_link(self, page):
        facebook_link = page.find("a", href=re.compile(r"facebook\.com"))
        if facebook_link:
            return facebook_link["href"]
        return None

    # Process the Facebook page
    def process_facebook_page(self, facebook_link):
        self.driver.get(facebook_link)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Close the modal window of logging in to Facebook
        try:
            close_button = self.driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]",
            )
            close_button.click()
        except:
            pass

        # Get the page source
        page_source = self.driver.page_source

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(page_source, "html.parser")

        # Find the block with the contact information
        info_block = soup.find(class_="x78zum5 x1n2onr6 xh8yej3")
        if info_block:
            # Iterate over each div element within the block
            for div in info_block.find_all("div"):
                # Check if the div element contains an email address
                if re.match(
                    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
                    div.text,
                ):
                    print(div.text)
                    break

    def close(self):
        self.driver.quit()


def main():
    scraper = Scraper()
    pages = ["calendly.com", "thejoint.com"]
    for page in pages:
        scraper.check_page(page)
    # Use scraper to check pages
    scraper.close()


if __name__ == "__main__":
    main()
