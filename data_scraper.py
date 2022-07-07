# import requirements

import time
import uuid

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from sqlalchemy import create_engine
from webdriver_manager.chrome import ChromeDriverManager

from security_keys import (
    password,
)  # build your own security_key.py file, please check readme


class NFT_scraper:

    """
    Collect NFT data based on ranking.
    """

    def __init__(self):

        """
        Initialise the NFT collections' table.
        """
        self.table = pd.DataFrame(
            columns=[
                "Rank",
                "Collection",
                "Volume",
                "24h %",
                "7d %",
                "Floor Price",
                "Owners",
                "Items",
            ]
        )
    def web_driver(self):

        """
        Prepare selenium chrome webdriver for scraping, set appropriate zoom of window,
         which is able to get all data of the page in two screen, initial screen and bottom screen.
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

    def collect_screen_data(self):

        """
        Collect dynamic website data from current screen
        """

        time.sleep(5)
        row_data = self.driver.find_elements(
            By.XPATH, '//*[@id="main"]/div/div[2]/div/div[3]'
        )
        data_split = [i.text for i in row_data][0].split("\n")
        row_table = [
            data_split[i*8:(i+1)*8] for i in range(int(len(data_split)/8))
        ]

        df = pd.DataFrame(
            row_table,
            columns=[
                "Rank",
                "Collection",
                "Volume",
                "24h %",
                "7d %",
                "Floor Price",
                "Owners",
                "Items",
            ],
        )
        return df

    def scrolling_screen_down(self):
        # scrolling down by 3200 vertically
        self.driver.execute_script("window.scrollBy(0 , 3200 );")

    def merging_table(self, df, df2):
        df = pd.concat([df, df2], ignore_index=False)
        df["Rank"] = df["Rank"].astype(str).astype(int)
        self.table = df.sort_values(by=["Rank"])
        return self.table

    def click_to_next_page(self):
        next = self.driver.find_element(
            By.XPATH, "//*[@id='main']/div/div[3]/button[2]"
        )
        self.driver.execute_script("arguments[0].click();", next)

    def save_table(self):
        self.table.to_csv("nft_ranking1.csv")

    def db_engine(self):
        DATABASE_TYPE = "postgresql"
        DBAPI = "psycopg2"
        # change to your own AWS RDS address
        ENDPOINT = "nfts.cftyhhxl7vmx.eu-west-2.rds.amazonaws.com"
        USER = "postgres"
        PASSWORD = password
        PORT = 5432
        DATABASE = "postgres"
        engine = create_engine(
            f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}"
        )
        return engine


if __name__ == "__main__":

    scraper = NFT_scraper()
    scraper.table = pd.DataFrame(
        columns=[
            "Rank",
            "Collection",
            "Volume",
            "24h %",
            "7d %",
            "Floor Price",
            "Owners",
            "Items",
        ]
    )
    driver = scraper.web_driver()

    for i in range(2):
        for j in range(5):
            time.sleep(3)
            data = scraper.collect_screen_data()
            scraper.merging_table(scraper.table, data)
            scraper.scrolling_screen_down()
        scraper.click_to_next_page()
    scraper.table = scraper.table.drop_duplicates("Rank")
    unique_ids = [uuid.uuid4() for i in range(len(scraper.table))]
    scraper.table["uuid"] = unique_ids
    scraper.table.to_csv("nft_ranking1.csv")
    scraper.driver.quit()
