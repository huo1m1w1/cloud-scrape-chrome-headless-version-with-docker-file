from sqlalchemy import create_engine
from  data_scraper import NFT_scraper
from  image_scraper import Image_scraper
import pandas as pd
import time
import uuid
from security_keys import password

"""
Collecting data and save to postgresql on AWS RDS
"""

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

DATABASE_TYPE = "postgresql"
DBAPI = "psycopg2"
# change to your own AWS RDS address
ENDPOINT = "nfts.cftyhhxl7vmx.eu-west-2.rds.amazonaws.com"
USER = "postgres"
PASSWORD = password  # enter your own password here
PORT = 5432
DATABASE = "postgres"
engine = create_engine(
    f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}"
)

engine.connect()
scraper.table.to_sql("NFTs", engine, if_exists="replace")

scraper.driver.quit()

"""
Collecting images and save to AWS S3
"""

scraper.table.drop_duplicates('Collection')
image_scrape = Image_scraper(scraper.table)
driver = image_scrape.Web_driver()
image_scrape.driver.execute_script("window.open('');")
image_scrape.driver.switch_to.window(image_scrape.driver.window_handles[0])

for i in range(2):

    collection = image_scrape.get_collection_title(i)
    links = image_scrape.get_image_addresses_of_the_collection(collection)
    path = "NFTs/" + str(scraper.table.iat[i, 8]) + "/" + str(scraper.table.iat[i, 8])
    image_scrape.collect_images(links, path)
image_scrape.driver.quit()

