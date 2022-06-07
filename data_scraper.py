# import requirements

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import uuid
import time
from selenium.webdriver.chrome.service import Service
import pandas as pd


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

    def Web_driver(self):

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
        options.add_argument("user-agent=[Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36]")
        s = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=s, options=options)               
        # self.driver.get("chrome://settings/")
        # self.driver.execute_script("chrome.settingsPrivate.setDefaultZoom(0.20);")
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
            data_split[i * 8 : (i + 1) * 8] for i in range(int(len(data_split) / 8))
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

        self.driver.execute_script("window.scrollBy(0 , 3200 );")


    # def scrolling_down_to_bottom(self):
    #     """
    #     scrolling down the page to bottom

    #     """

    #     html = self.driver.find_element_by_tag_name("html")
    #     html.send_keys(Keys.END)
    #     time.sleep(1)

    def merging_table(self, df, df2):
        df = pd.concat([df, df2], ignore_index=False)
        # df = df.drop_duplicates()
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
    driver = scraper.Web_driver()

    for i in range(2):
        
        for i in range(5):
            time.sleep(3)
            data = scraper.collect_screen_data()
            scraper.merging_table(scraper.table, data)
            scraper.scrolling_screen_down()
        scraper.click_to_next_page()
    scraper.table.drop_duplicates('Collection')
    unique_ids = [uuid.uuid4() for i in range(len(scraper.table))]
    scraper.table["uuid"] = unique_ids
    scraper.table.to_csv(
        'nft_ranking1.csv'
    )
    scraper.driver.quit()
