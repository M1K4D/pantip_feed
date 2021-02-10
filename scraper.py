from typing import Text
from bs4 import BeautifulSoup
import requests as req
import feedparser
import pandas as pd
import os
import time
from yaspin import yaspin


def find(arr, title):
    for x in arr:
        if str(x["title"]) == str(title):
            return True
        else:
            return False


def pantip_extract(arrs):
    feed = feedparser.parse('https://pantip.com/forum/feed')
    new_items = []
  # print(len(arrs))
    if len(arrs) == 0:
        for item in feed.entries:
            _item = {}
            _item['title'] = item.title
            _item['description'] = item.summary
            _item['link'] = item.link
            _item['published'] = item.published
            new_items.append(_item)
    else:
        for item in feed.entries:
            title = find(arrs, item.title)
            # print(title)
            if not title:
                _item = {}
                _item['title'] = item.title
                _item['description'] = item.summary
                _item['link'] = item.link
                _item['published'] = item.published
                new_items.append(_item)
    return new_items


pantip_data = []
with yaspin(text='scraping..........'):
    while True:
        t = time.time()
        result = time.localtime(t)
        data = pantip_extract(pantip_data)
        # print("result_tm_hour : ", result.tm_hour)
        pantip_data.extend(data)
        if result.tm_hour >= 18 and result.tm_min >= 55:
            print("Finish")
            break
        time.sleep(60)

data_clean = []
for i in range(len(pantip_data)):
    if pantip_data[i] not in pantip_data[i + 1:]:
        data_clean.append(pantip_data[i])

data_frame = pd.DataFrame(
    data_clean, columns=['title', 'description', 'link', 'published'])
print("data frame length : ", len(data_frame))


path = os.getcwd()
print(path)
data_frame.to_csv(path + '/export_dataframe.csv', header=True)
