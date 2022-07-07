import time

import boto3
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from security_keys import access_key, secret_key


class Image_scraper:

    """
    Collect NFT images from OPENSEA.IO, based on the ranking of collections.
    """

    def __init__(self, df, url="https://opensea.io/rankings"):
        self.url = url
        self.second_url = ""
        self.df = df

    def web_driver(self):

        """
        Preparing selenium chrome webdriver
        """

        url = "https://opensea.io/rankings"
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920x1080")
        options.add_argument("start-maximised")
        options.add_argument(
            "user-agent=[Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36]"
        )
        s = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=s, options=options)

        return self.driver.get(url)

    def get_collection_title(self, index):

        """
        Get collections from previous collected ranking data table.
        """

        return self.df["Collection"].iloc[index]

    def get_image_addresses_of_the_collection(self, collection):

        """
        Click and open collection page, maximise the window,
        scroll the page to an appropriate level,
        and get corresponding images addresses
        """
        time.sleep(2)
        elem = self.driver.find_element(
            By.CSS_SELECTOR,
            '#__next > div > div.sc-d040ow-3.kCqGcl > nav > div.sc-1xf18x6-0.bSaLsG > div.sc-1xf18x6-0.sc-1twd32i-0.hzdGQw.kKpYwv > div > div > div > div > div > input[type=text]',
        )

        elem.send_keys(collection)
        time.sleep(6)
        self.driver.find_element(By.XPATH, '//*[@id="NavSearch--results"]/li[2]/a/div[2]').click()

        # scroll the page to an appropriate level
        self.driver.maximize_window()
        time.sleep(4)
        level = self.driver.find_element(
            By.CSS_SELECTOR,
            "#main > div > div > div.sc-1xf18x6-0.sc-z0wxa3-0.hnKAL.hWJuuu > div > div.sc-1po1rbf-6.bUKivE > div.sc-1xf18x6-0.cPWSa-d.AssetSearchView--main > div.AssetSearchView--results.collection--results.AssetSearchView--results--phoenix > div.fresnel-container.fresnel-greaterThanOrEqual-md > div",
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

        self.driver.switch_to.window(self.driver.window_handles[1])
        session = boto3.Session(aws_access_key_id=access_key, aws_secret_access_key=secret_key)
        s3 = session.resource("s3")
        for i in range(len(links) - 1):
            self.driver.get(links[i + 1])

            # switch to the link in a new tab by sending key strokes on the element
            time.sleep(1)
            image = self.driver.find_element(
                By.XPATH,
                "//*[@id='main']/div/div/div/div[1]/div/div[1]/div[1]/article/div/div/div/div/img",
            )
            r = requests.get(image.get_attribute("src"))
            file_path = path + str(i + 1) + ".jpg"
            object = s3.Object("cloud-scraper", file_path)
            object.put(Body=r.content)
            time.sleep(5)
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.get(self.url)

    def collect_images1(self, links, path):
        """
        Open another window for each NFT item, get the image and save to drive.
        The reason for doing this way is because the iamge quality on the item own page better than on
        the collection page.
        """

        # Switch to the new window
        self.driver.switch_to.window(self.driver.window_handles[1])

        for i in range(len(links) - 1):
            self.driver.get(links[i + 1])
            time.sleep(1)
            image = self.driver.find_element(
                By.XPATH,
                "//*[@id='main']/div/div/div/div[1]/div/div[1]/div[1]/article/div/div/div/div/img",
            )
            r = requests.get(image.get_attribute("src"))
            with open(path + str(i + 1) + ".jpg", "wb") as f:
                f.write(r.content)
        self.driver.switch_to.window(self.driver.window_handles[0])


if __name__ == "__main__":
    df = pd.read_csv("nft_ranking1.csv", index_col=0)  # this is going introduce from rds or inter memory.
    image_scraper = Image_scraper(df)
    driver = image_scraper.web_driver()
    image_scraper.driver.execute_script("window.open('');")
    image_scraper.driver.switch_to.window(image_scraper.driver.window_handles[0])
    time.sleep(1)

    for i in range(2):
        collection = image_scraper.get_collection_title(i)

        links = image_scraper.get_image_addresses_of_the_collection(collection)
        path = "NFTs/" + df.iat[i, 8] + "/" + df.iat[i, 8]
        image_scraper.collect_images(links, path)
    image_scraper.driver.quit()
