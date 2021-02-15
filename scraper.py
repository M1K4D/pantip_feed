from typing import Text
from bs4 import BeautifulSoup
import requests
import feedparser
import pandas as pd
import time
import threading as thr
import multiprocessing as mp
import os
from yaspin import yaspin


def pantip_extract():
    feed = feedparser.parse('https://pantip.com/forum/feed')
    new_items = []
    for item in feed.entries:
        _item = {}
        _item['title'] = item.title
        _item['description'] = item.summary
        _item['link'] = item.link
        _item['published'] = item.published

        new_items.append(_item)
    return new_items


pantip_data = []


def get_data():
    pantip_data = []
    with yaspin(text='scraping..........'):
        while True:
            data = pantip_extract()
            pantip_data.extend(data)

            remove_dup = []
            for i in range(len(pantip_data)):
                if pantip_data[i] not in pantip_data[i + 1:]:
                    remove_dup.append(pantip_data[i])

            data_frame = pd.DataFrame(
                remove_dup, columns=['title', 'description', 'link', 'published'])
            print("data length : ", len(data_frame))
            path = os.getcwd()
            data_frame.to_csv(path + '/raw_dataframe.csv', header=True)
            time.sleep(60)


get_data()
