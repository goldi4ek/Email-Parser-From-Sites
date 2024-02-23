from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import ProxyType
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup
import re
import time


class Scraper:
    def __init__(self):
        # Set up the Chrome driver
        options = Options()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("--headless")  # Run Chrome in headless mode
        service = Service("chromedriver.exe")
        self.driver = Chrome(service=service, options=options)

    # Check the page for an email address
    def check_page(self, url):
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
                        self.process_facebook_page(facebook_link)
                    else:
                        print("No email and facebook found")
                        return None
            else:
                print(
                    f"Failed to load page: {url} with status code {response.status_code}"
                )
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
                    return div.text
            print("No email found on Facebook page")
            return None

    def close(self):
        self.driver.quit()


def main():
    scraper = Scraper()
    pages = [
        "milleniachiropracticorlando.com",
        "milleniachiropracticorlando.com",
        "orlandochiropractic.com",
        "chiropracticspineinjury.com",
        "reid-chiro.com",
        "chiropractorwellington.com",
        "chiropractorwellington.com",
        "omgchiro.com",
        "tampacentralchiropractic.com",
        "southorlandochiro.com",
        "encompasschiropractic.com",
        "online-chat.io",
        "spineandjointofswfl.com",
    ]

    pages_and_emails = {}

    i = 0
    for page in pages:
        if page not in pages_and_emails:
            print(i, " ", page)
            pages_and_emails[page] = scraper.check_page(page)
            i += 1

    print(pages_and_emails)
    # Use scraper to check pages
    scraper.close()


if __name__ == "__main__":
    main()

""" 
        "calendly.com",
        "thejoint.com",
        "bocachiropracticsw.com",
        "lakenonachiropractic.com",
        "calendly.com",
        "thejoint.com",
        "bocachiropracticsw.com",
        "bocachiropracticsw.com",
        "lakenonachiropractic.com",
        "orangewellness.com",
        "orangewellness.com",
        "chiropractorpalmcoast.com",
        "chiropractorpalmcoast.com",
        "riverviewchiropracticcenter.com",
        "advancedspinetherapy.com",
        "drrickbruns.com",
        "ormondfamilychiro.com",
        "ormondfamilychiro.com",
        "nightlightchiropractic.com",
        "nightlightchiropractic.com",
        "acomhealth.com",
        "wesleychapelchiropractor.com",
        "orlandocityhealth.com",
        "totalhealthnaples.com",
        "orangewellness.com",
        "orangewellness.com",
        "hochmanchiro.com",
        "yocale.com",
        "chiropractorsinkendall.com",
        "lbvchiro.com",
        "lbvchiro.com",
        "zocdoc.com",
        "winterparkchiropractor.com",
        "patienthealthcenters.org",
        "procarefl.com",
        "vivahealthcenters.com",
        "vivahealthcenters.com",
        "getchiro.net",
        "drneilspanier.com",
        "miramarchirorehab.com",
        "miramarchirorehab.com",
        "reesechiro.com",
        "nuspine.com",
        "thejoint.com",
        "miamichiropracticwellness.com",
        "stgermainchiropractic.com",
        "downtownmiamichiropractor.com",
        "simplybook.me",
        "integratedchiropracticofboca.com",
        "janeapp.com",
        "foundationflorida.com",
        "cobbrehabwellness.com",
        "zocdoc.com",
        "carewellness.org",
        "harboursidechiropractic.com",
        "nordikchiropractic.com",
        "nordikchiropractic.com",
        "drzevtv.com",
        "fortlauderdalewhiplash.com",
        "fortlauderdalewhiplash.com",
        "lakelandsfamilychiropractic.com",
        "stephensclinic.com",
        "stephensclinic.com",
        "schedulista.com",
        "jaxbax.com",
        "themiamichiropractor.com",
        "floridachiropractor.com",
        "mychirotouch.com",
        "chiropractorinmiami.com",
        "praglechiropractictallahassee.com",
        "pinnaclebradenton.com",
        "calendly.com",
        "ptcmiami.com",
        "sports-spine.com",
        "flspineandinjury.com",
        "melbournechiropractic.net",
        "flspineandinjury.com",
        "flspineandinjury.com",
        "ocalainjurycenter.com",
        "chiro.city",
        "drleighsierra.com",
        "drmichaelnewman.com",
        "drmichaelnewman.com",
        "marshallwebsterchiropractor.com",
        "verobeachchiropractic.com",
        "murdockwellness.com",
        "chiropractorjupiterfl.com",
        "chiropractorjupiterfl.com",
        "michaelsavignanochiropractor.com",
        "drericnye.com", 
        "drbochiro.com",
        "jacklynady.com",
        "zocdoc.com",
        "chiropractorhialeah.com",
        "grappinclinic.com",
        "totalchiropracticcare.com",
        "thespineclinic.com",
        "thespineclinic.com",
        "snyderchiropractic.com",
        "snyderchiropractic.com",
        "ocalafamilychiropractic.com",
        "bohnchiropractic.com",
        "spineandrehabcenters.com",
        "clientsecure.me",
        "ledbetterchiropractic.com",
        "mynewhopechiro.com",
        "communitychiropractor.com",
        "communitychiropractor.com",
        "chirotouch.com",
        "drsalvatoreromano.com",
        "chiropractorkissimmee.com",
        "grappinclinic.com",
        "drdavidscoppa.com",
        "wpbchiropractor.com",
        "kingdomchiropractic.com",
        "facebook.com",
        "soflochiro.com",
        "drconradblog.com",
        "myhuffmanchiropractic.com",
        "ajchiropractors.com",
        "sarasotawellness.com",
        "pembrokepines-chiropractor.com",
        "grappinclinic.com",
        "genbook.com",
        "praglechiropractictallahassee.com",
        "brecheractivehealth.com",
        "cafeoflifewellness.com",
        "cafeoflifewellness.com",
        "100percentchiropractic.com",
        "100percentchiropractic.com",
        "feelamazing.com",
        "feelamazing.com",
        "drauchter.com",
        "drauchter.com",
        "thesourcestpete.com",
        "thesourcestpete.com",
        "currentchiropractic.com",
        "100percentchiropractic.com",
        "100percentchiropractic.com",
        "maxliving.com",
        "maxliving.com",
        "janeapp.com",
        "livefreechiropractic.com",
        "destinchiros.com",
        "grovechiropractic.com",
        "fortmyerschirostudio.com",
        "fortmyerschirostudio.com",
        "healthsourcechiro.com",
        "healthsourcechiro.com",
        "phancore.com",
        "phancore.com",
        "janeapp.com",
        "spinelifechiropractic.com",
        "healinghandssportschiro.com",
        "northfortmyerschiropractor.com",
        "fusionchirospa.com",
        "polkaccidentinjury.com",
        "baileyhealthsolutions.com",
        "baileyhealthsolutions.com",
        "meridian-wellness.com",
        "meridian-wellness.com",
        "chiropractorwinterhaven.com",
        "chiropractorwinterhaven.com",
        "seasidespinedestin.com",
        "pcchiropracticcenter.com",
        "drmichaelshaffer.business.site",
        "drashleydixon.com",
        "drashleydixon.com",
        "grangerhealth.com",
        "chirofitsunrise.com",
        "chirofitsunrise.com",
        "smithfamilychiro.net",
        "vidachiropracticmiami.com",
        "thevillagechiropractor.com",
        "drobnicassoc.com",
        "straighttohealth.com",
        "straighttohealth.com",
        "vitalitycenterjax.com",
        "vitalitycenterjax.com",
        "merrittislandchiropractor.com",
        "merrittislandchiropractor.com",
        "sarasotaflchiropractor.com",
        "soflochiro.com",
        "soflochiro.com",
        "spineandsportstherapyonline.com",
        "spineandsportstherapyonline.com",
        "pioneernsb.com",
        "amazingspinecare.com",
        "amazingspinecare.com",
        "pipdoc.com",
        "momentuminjury.com",
        "olairechiropractic.com",
        "bayareawellnesscenter.com",
        "bayareawellnesscenter.com",
        "chiromatrixbase.com",
        "jaxchirorehab.com",
        "radiantwellnesscenter.com",
        "radiantwellnesscenter.com",
        "janeapp.com",
        "stjohnschiropractic.com",
        "janeapp.com",
        "apexchiro-rehab.janeapp.com",
        "thewayofwellness.com",
        "powerchiropracticmiami.com",
        "powerchiropracticmiami.com",
        "sandbchiropractic.com",
        "sandbchiropractic.com",
        "valdostachiropractic.com",
        "valdostachiropractic.com",
        "orlandoresortschiro.com",
        "janeapp.com",
        "chiropalmbeach.com",
        "lakeschirofl.com",
        "lakeschirofl.com",
        "gainesvilleflchiro.com",
        "newjourneychiropractic.com",
        "newjourneychiropractic.com",
        "drbrentcoons.com",
        "drcodybooth.com",
        "bfcchiro.com",
        "fogartychiropractic.com",
        "castellichiro.com",
        "castellichiro.com",
        "corsentinochiro.com",
        "corsentinochiro.com",
        "simpsonmedical.com",
        "christiechiropractic.com",
        "christiechiropractic.com",
        "opachichwellness.com",
        "opachichwellnesscenter.com",
        "prospectchiro.com",
        "prospectchiro.com",
        "avenueonechiropractic.com",
        "avenueonehealthcenter.com",
        "zingitapps.com",
        "alessifunctionalhealth.com",
        "facebook.com",
        "orlandoinjurymedicine.com",
        "absolutelyadvanced.com",
        "absolutelyadvanced.com",
        "essentialmb.com",
        "winterparkdisccenter.com",
        "winterparkdisccenter.com",
        "needchiropractic.com",
        "needchiropractic.com",
        "orlandochiropracticrehab.com",
        "lakewoodchiropracticjax.com",
        "lakewoodchiropracticjax.com",
        "chiropractorlakemary.com",
        "chiropractorlakemary.com",
        "bensachiropractic.com",
        "bensachiropractic.com",
        "edwinrobertschiro.com",
        "edwinrobertschiro.com",
        "411orlandobackpain.com",
        "suncoastchiropractic.com",
        "drwassermann.com",
        "drwassermann.com",
        "chirocareflorida.com",
        "oznerfamilychiropractic.com",
        "oznerfamilychiropractic.com",
        "sunsetchirotampa.com",
        "sunsetchirotampa.com",
        "janeapp.com",
        "anchorsportschiro.com",
        "luchachiropractic.care",
        "zocdoc.com",
        "linktr.ee",
        "worldhealthwellness.com",
        "comprehensivehealthflorida.com",
        "floridahealthandchiropracticmedicine.com",
        "chirocareflorida.com",
        "northflorida-chiro.com",
        "dryingling.com",
        "myfcrc.com",
        "sflachiro.com",
        "heartoffloridachiropractic.com",
        "heartoffloridachiropractic.com",
        "floridachiropracticinstitute.net",
        "floridacoastchiropractic.com",
        "stgermainchiropractic.com",
        "newcitychiro.com",
        "floridachiropracticcare.com",
        "mynewhopechiro.com",
        "cclchiro.com",
        "cclchiro.com",
        "floridaspine.us",
        "mylutzchiropractor.com",
        "zocdoc.com",
        "specialtychiropractic.com",
        "drryanbriggs.com",
        "drryanbriggs.com",
        "onpointchiroflorida.com",
        "onpointchiroflorida.com",
        "chirocareflorida.com",
        "callmychiropractor.com",
        "callmychiropractor.com",
        "healthfirstcn.com",
        "healthfirstcn.com",
        "northfloridachiropracticphysicaltherapy.com",
        "eustischiro.com",
        "michaelsavignanochiropractor.com",
        "michaelsavignanochiropractor.com",
        "setmore.com",
        "painfreechiropractic.net",
        "facebook.com",
        "sfloridaspine.com",
        "doublebranchchiropractic.com",
        "bacpainfree.com",
        "stgermainchiropractic.com",
        "southfloridadiscandspine.com",
        "kaizenchiropracticsolutions.com",
        "kaizenchiropracticsolutions.com",
        "seminolechiropracticcenter.com",
        "seminolechiropracticcenter.com",
        "simplychiropracticpalmbeach.com",
        "floridaspineandwellness.com",
        "spinalsolutionsfl.com",
        "flcclearwater.com",
        "chiropracticofnaples.com",
        "flspinalcare.com",
        "clearwaterspine.com",
        "100percentchiropractic.com",
        "100percentchiropractic.com",
        "painresults.com",
        "painresults.com",
        "changingtideschiro.com",
        "janeapp.com",
        "shred.doctor",
        "sfmwc.com",
        "sfmwc.com",
        "pineswestchiropractic.com",
        "cornerstonechiropracticrehab.com",
        "cornerstonechiropracticrehab.com",
        "floridabackandneckpain.com",
        "floridaspineandinjury.com",
        "brandonautoaccident.com",
        "parklandchiropractic.com",
        "parklandchiropractic.com",
        "hartleychiropracticsaintaugustine.com",
        "hartleychiropracticsaintaugustine.com",
        "affordablechiro.net",
        "expresslifechiro.com",
        "expresslifechiro.com",
        "slighchiropractic.com",
        "patonchiropractic.com",
        "healthytallahassee.com",
        "flspinedisc.com",
        "flspinedisc.com",
        "flpwellness.com",
        "flpwellness.com",
        """
