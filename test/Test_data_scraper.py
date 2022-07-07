import os
import sys
import time
import unittest
import pandas as pd 

p = os.path.abspath(".")
sys.path.insert(1, p)

# from data_scraper import NFT_scraper as scraper
import data_scraper


class TestStringMethods(unittest.TestCase):

    def test_data_collection(self):
        scraper = data_scraper.NFT_scraper()
        scraper.web_driver()
        for j in range(5):
            time.sleep(3)
            data = scraper.collect_screen_data()
            scraper.merging_table(scraper.table, data)
            scraper.scrolling_screen_down()

        time.sleep(4)
        scraper.click_to_next_page()
        data = scraper.collect_screen_data()
        scraper.merging_table(scraper.table, data)

        # test 1 tp check if the scrape has collect data of ranking 1
        scraper.table.to_csv("nft_ranking1.csv")
        self.assertEqual(
            scraper.table[scraper.table["Rank"] == 1]["Collection"].values[0],
            "ENS: Ethereum Name Service",
        )  # 'goblintown.wtf' should be the name of ranking 1 NFT

        # test 2 to check if the scraper scrolling the screen down to the bottom and collecting last dataset on that page.
        self.assertEqual(
            scraper.table[scraper.table["Rank"] == 100]["Collection"].values[0],
            "gmDAO token",
        )  # make sure it is the name of ranking 100 NFT

        # test 3 to check if the scraper click to next page and collect first data from that page.
        self.assertEqual(
            scraper.table[scraper.table["Rank"] == 101]["Collection"].values[0],
            "THE SNKRZ NFT",  # make sure it is NFT name of ranking 101
        )


if __name__ == "__main__":
    unittest.main()
