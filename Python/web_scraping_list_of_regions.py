import pandas as pd
from functools import reduce
import scrapy
from scrapy.crawler import CrawlerProcess

class SpiderCoopWellBeing(scrapy.Spider):
    
    name="Coop Well-being Spider"

    def start_requests(self):

        string_url="https://geolytixmapp.com/coopwellbeing/api/query?template=get_lad_from_region&region={placeholder_region}"

        list_regions=["East Midlands", "Eastern", "London", "North East", "North West", "Scotland", "South East", "South West", "Wales", "West Midlands", "Yorkshire and The Humber"] # Northern Ireland does not have LADs

        for region in list_regions:

            url=string_url.format(placeholder_region=region)

            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        json_LAD=response.json()

        df_LAD=pd.DataFrame.from_dict(json_LAD, orient="columns")

        list_df_LAD.append(df_LAD)

list_df_LAD=[]

process=CrawlerProcess()
process.crawl(SpiderCoopWellBeing)
process.start()

df_LAD_concatenated=pd.concat(list_df_LAD) 

# df_LAD_concatenated.to_csv("LAD_concatenated.csv", index=False)
