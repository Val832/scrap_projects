import re 
import pandas as pd 
import requests
import numpy as np
from tools import Crawler, tqdm_executor_map, FetchData, MissingTable

import concurrent.futures

BASE  =  "https://www.formula1.com" 
URL = ("https://www.formula1.com/en/results.html/2023/races/1141/bahrain/race-result.html")

res = Crawler.extract_html(URL)
href = Crawler.find(res, 'a', attrs_key= "data-name", attrs_value="year")

urls_year = []

for i in href :
    
    link = i.get('href')
    if link : 
        urls_year.append(BASE+link)


urls_gp = []
for year in urls_year : 

    req = Crawler.extract_html(year)
    races = Crawler.find(res, 'a', attrs_key= "data-name", attrs_value="meetingKey")

    for race in races[1:] : 
        link = race.get('href')
        urls_gp.append(BASE+link)

na_table = MissingTable.f1_missing_table(URL)
urls_gp = urls_gp[:3]
sessions = [requests.Session() for _ in range(len(urls_gp))]
with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    all_df = tqdm_executor_map(executor, FetchData.fetch_f1_data, urls_gp, 
                                     [na_table]*len(urls_gp), sessions, total = len(urls_gp))

all_df = [df.reset_index(drop=True) for df in all_df]
df = pd.concat(all_df, ignore_index=True)


df.to_csv("/Users/valentinnaud/Desktop/scrap_projects/data/f1/f1_data.csv")
