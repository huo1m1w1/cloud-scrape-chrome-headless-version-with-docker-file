        
        
    #     imsc.Web_driver()
    #     imsc.collect_screen_data()
    #     # scraper.merging_table(scraper.table, data)
    #     self.assertEqual(data[data['Rank']=='1']['Collection'].values[0], 'goblintown.wtf') # 'goblintown.wtf' should be the name of ranking 1 NFT
    #     imsc.Web_driver()
    #     imsc.driver.execute_script("window.open('');")
    #     imsc.driver.switch_to.window(imsc.driver.window_handles[0])
    
    
    
    # def test_merging_table(self):
    #     scraper = data_scraper.NFT_scraper()
    #     scraper.table = pd.DataFrame(
    #         columns=[
    #         "Rank",
    #         "Collection",
    #         "Volume",
    #         "24h %",
    #         "7d %",
    #         "Floor Price",
    #         "Owners",
    #         "Items",
    #     ]
    #     )
    #     scraper.Web_driver()
    #     # data=scraper.collect_screen_data()
    #     # scraper.merging_table(scraper.table, data)
    #     scraper.scrolling_down_to_bottom()
    #     time.sleep(2)
    #     data=scraper.collect_screen_data()
    #     # scraper.merging_table(scraper.table, data)
    #     self.assertEqual(data[data['Rank']=='100']['Collection'].values[0], 'Ape Reunion') # 'Town Star' should be the name of ranking 100 NFT
    


    # def test_next_page_data_collection(self):
    #     scraper = data_scraper.NFT_scraper()
    #     scraper.Web_driver()
    #     scraper.scrolling_down_to_bottom()
    #     time.sleep(4)
    #     scraper.click_to_next_page()
    #     data=scraper.collect_screen_data()
    #     # scraper.merging_table(scraper.table, data)
    #     # make sure 'GNSS Art by MGXS' is the name of ranking 101 NFT
    #     self.assertEqual(scraper.table[scraper.table['Rank']=='101']['Collection'].values[0], 'GNSS Art by MGXS')
