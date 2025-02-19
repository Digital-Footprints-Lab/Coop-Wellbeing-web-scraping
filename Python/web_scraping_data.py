import pandas as pd
from numpy import random
from time import sleep
from functools import reduce
import scrapy
from scrapy.crawler import CrawlerProcess

class SpiderCoopWellBeing(scrapy.Spider):
    
    name="Coop Well-being Spider"

    def start_requests(self):

        string_url="https://geolytixmapp.com/coopwellbeing/api/query?name={placeholder_LAD}&template=admin_{placeholder_domain}&locale=wellbeing&layer=lad"

        df_LAD_concatenated=pd.read_csv("./LAD_concatenated.csv")

        list_well_being_domains=["index", "people", "place", "relationships"]

        for LAD in df_LAD_concatenated.lad_name:

            for domain in list_well_being_domains:

                url=string_url.format(placeholder_LAD=LAD, placeholder_domain=domain)

                sleep(random.uniform(0, 1))

                yield scrapy.Request(url=url, callback=self.parse, cb_kwargs=dict(domain=domain, LAD=LAD))

    def parse(self, response, domain, LAD):

        json_well_being=response.json()

        df_well_being=pd.DataFrame.from_dict(json_well_being, orient="columns")

        df_well_being=df_well_being.assign(LAD=LAD)

        dict_df_well_being[domain].append(df_well_being)

dict_df_well_being={"index": [], "people": [], "place": [], "relationships": []}
list_df_well_being_concatenated=[]

process=CrawlerProcess()
process.crawl(SpiderCoopWellBeing)
process.start()

for domain in dict_df_well_being:

    df_well_being_concatenated=pd.concat(dict_df_well_being[domain])

    list_df_well_being_concatenated.append(df_well_being_concatenated)

df_well_being_grand=reduce(lambda df1, df2: pd.merge(df1, df2, on=["id", "dd_name", "LAD"], how="outer"), list_df_well_being_concatenated)

# df_well_being_grand.to_csv("well_being_grand.csv", index=False)
