import unittest
import pandas as pd
import os, sys
p = os.path.abspath(".")
sys.path.insert(1, p)
import image_scraper
# from data_scraper import NFT_scraper as scraper

class TestStringMethods(unittest.TestCase):
    def test_get_collection_title(self):

        df = pd.read_csv("nft_ranking1.csv", index_col=0)
        imsc = image_scraper.Image_scraper(df)
        title_list = [imsc.get_collection_title(i) for i in range(10)]
        self.assertEqual(title_list[0], df[df["Rank"] == 1]["Collection"].values[0])

    def test_get_image_addresses_of_the_collection(self):
        df = pd.read_csv("nft_ranking1.csv", index_col=0)
        imsc = image_scraper.Image_scraper(df)
        title_list = [imsc.get_collection_title(i) for i in range(10)]
        imsc.web_driver()
        print(title_list[0])
        image_addresses = imsc.get_image_addresses_of_the_collection(title_list[0])
        self.assertIn("https://opensea.io/assets/ethereum/0x57f1887a8bf19b14fc0df6fd9b2acc9af147ea85/81911658944144762750121759600275738527811859523043300904877251018945625872069",
            image_addresses,
            
        )  # make sure this is the first image address of ranking 1 NFT


if __name__ == "__main__":
    unittest.main()
