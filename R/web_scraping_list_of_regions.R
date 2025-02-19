library(data.table)
library(magrittr)
library(rvest)
library(jsonlite)

string_url<-"https://geolytixmapp.com/coopwellbeing/api/query?template=get_lad_from_region&region={placeholder_region}"

array_regions<-c("East Midlands", "Eastern", "London", "North East", "North West", "Scotland", "South East", "South West", "Wales", "West Midlands", "Yorkshire and The Humber")

df_LAD_grand<-data.table()

for (region in array_regions){
    
    url<-gsub("\\{placeholder_region\\}", region, string_url) %>% gsub(" ", "%20", .)
        
    df_LAD<-fromJSON(url)
    
    df_LAD_grand<-rbind(df_LAD_grand, df_LAD)
    
}

# save(df_LAD_grand, file="./LAD_grand.RData")
