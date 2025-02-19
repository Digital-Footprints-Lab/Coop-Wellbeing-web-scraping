library(data.table)
library(magrittr)
library(rvest)
library(jsonlite)

string_url="https://geolytixmapp.com/coopwellbeing/api/query?name={placeholder_LAD}&template=admin_{placeholder_domain}&locale=wellbeing&layer=lad"

load("./LAD_grand.RData")

array_well_being_domains=c("index", "people", "place", "relationships")

df_wellbeing_grand<-data.table()

for (LAD in df_LAD_grand$lad_name){
    
    df_wellbeing_LAD<-data.table(cbind(id=NA, dd_name=NA))
    
    for (domain in array_well_being_domains){
        
        url<-gsub("\\{placeholder_LAD\\}", LAD, string_url) %>% gsub("\\{placeholder_domain\\}", domain, .) %>% gsub(" ", "%20", .)
        
        Sys.sleep(runif(1))
        
        df_wellbeing<-tryCatch(fromJSON(url), error=function(e) {return(data.table(cbind(id=NA, dd_name=NA)))})

        df_wellbeing_LAD %<>% merge(., df_wellbeing, by=c("id", "dd_name"), all=TRUE)
        
    }
    
    df_wellbeing_grand<-rbind(df_wellbeing_grand, df_wellbeing_LAD, fill=TRUE)
    
    df_wellbeing_grand %<>% na.omit(., cols=c("id", "dd_name"))
    
}

# save(df_wellbeing_grand, file="./wellbeing_grand.RData")
