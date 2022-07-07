from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
from selenium.webdriver.chrome.service import Service
import pandas as pd
import boto3


class Image_scraper:
    """
    Collect NFT images from OPENSEA.IO, based on the ranking of collections.
    """

    def __init__(self, df, url="https://opensea.io/rankings"):
        self.url = url
        self.second_url = ""
        self.df = df

    def Web_driver(self):

        """
        Preparing selenium chrome webdriver
        """

        options = Options()
        options.headless = True
        options.add_experimental_option("detach", True)
        s = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=s, options=options)

        return self.driver.get(self.url)

    def get_collection_title(self, index):

        """
        Get collections from previous collected ranking data table.
        """

        return self.df.iat[index, 1]  # Using .iat attribute

    def get_image_addresses_of_the_collection(self, collection):

        """
        Click and open collection page, maximise the window,
        scroll the page to an appropriate level,
        and get corresponding images addresses
        """
        time.sleep(2)
        elem = self.driver.find_element(
            By.CSS_SELECTOR,
            # "#__next > div > div.Navbarreact__DivContainer-sc-d040ow-2.gRSAHO > nav > div.Blockreact__Block-sc-1xf18x6-0.bYwkCJ > div > div > div > input[type=text]",
            "#__next > div > div.sc-d040ow-2.ylIie > nav > div.sc-1xf18x6-0.hJUbCF > div > div > div > input[type=text]",
        )
        elem.send_keys(collection)
        time.sleep(2)
        self.driver.find_element(
            By.XPATH,  # "//*[@id='NavSearch--results']/li[2]/a/div[2]/span"
            '//*[@id="NavSearch--results"]/li[2]/a/div[2]/div/div/span',
        ).click()

        # scroll the page to an appropriate level
        self.driver.maximize_window()
        time.sleep(2)
        level = self.driver.find_element(
            By.CSS_SELECTOR,
            # "#main > div > div > div.Blockreact__Block-sc-1xf18x6-0.elqhCm > div > div > div > div.AssetSearchView--results.collection--results > div.Blockreact__Block-sc-1xf18x6-0.elqhCm.AssetsSearchView--assets > div.fresnel-container.fresnel-greaterThanOrEqual-sm > div > div",
            "#main > div > div > div.sc-1xf18x6-0.sc-z0wxa3-0.gczeyg.bEVkke > div > div.sc-1po1rbf-6.bUKivE > div.sc-1xf18x6-0.bozbIq.AssetSearchView--main > div.AssetSearchView--results.collection--results.AssetSearchView--results--phoenix > div.sc-1xf18x6-0.hDbqle.AssetsSearchView--assets",
        )

        self.driver.execute_script("arguments[0].scrollIntoView(true);", level)

        time.sleep(2)
        d = self.driver.find_elements(By.XPATH, '//div[@role = "gridcell"]')

        d = self.driver.find_elements(By.XPATH, "//a[contains(@href, 'assets')]")

        links = [i.get_attribute("href") for i in d]

        return links

    def collect_images(self, links, path):
        """
        Open another window for each NFT item, get the image and save to drive.
        The reason for doing this way is because the iamge quality on the
        item own page better than on the collection page.
        """
        # open seconf window/tag,
        # self.driver.execute_script("window.open('');")
        # Switch to the new window
        self.driver.switch_to.window(self.driver.window_handles[1])

        session = boto3.Session(
            aws_access_key_id=access_key, aws_secret_access_key=secret_key
        )

        s3 = session.resource("s3")

        for i in range(len(links) - 1):
            self.driver.get(links[i + 1])
            # switch to the link in a new tab by sending key strokes on the element
            # d = self.driver.find_elements(By.XPATH, '//div[@role = "gridcell"]')
            time.sleep(1)
            image = self.driver.find_element(
                By.XPATH,
                "//*[@id='main']/div/div/div/div[1]/div/div[1]/div[1]/article/div/div/div/div/img",
            )
            r = requests.get(image.get_attribute("src"))
            file_path = path + str(i + 1) + ".jpg"
            object = s3.Object("cloud-scraper", file_path)
            result = object.put(Body=r.content)
            time.sleep(5)
        self.driver.switch_to.window(self.driver.window_handles[0])


if __name__ == "__main__":
    df = pd.read_csv(
        "nft_ranking1.csv", index_col=0
    )  # this is going introduce from rds or inter memory.
    image_scraper = Image_scraper(df)
    driver = image_scraper.Web_driver()
    image_scraper.driver.execute_script("window.open('');")
    image_scraper.driver.switch_to.window(image_scraper.driver.window_handles[0])

    for i in range(2):
        collection = image_scraper.get_collection_title(i)

        links = image_scraper.get_image_addresses_of_the_collection(collection)
        path = "NFTs/" + df.iat[i, 8] + "/" + df.iat[i, 8]
        image_scraper.collect_images(links, path)
    image_scraper.driver.quit()