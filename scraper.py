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
# import deepcut


def pantip_extract(keywords):
    feed = feedparser.parse('https://pantip.com/forum/feed')
    new_items = []
    if len(keywords) == 0:
        for item in feed.entries:
            _item = {}
            _item['title'] = item.title
            _item['description'] = item.summary
            _item['link'] = item.link
            _item['published'] = item.published

            new_items.append(_item)
    else:
        for item in feed.entries:
            keywords_match = False
            _item = {}
            _item['title'] = item.title
            _item['description'] = item.summary
            _item['link'] = item.link
            _item['published'] = item.published

            for keyword in keywords:
                title = item.title
                find = title.find(keyword)
                if find >= 0:
                    keywords_match = True

            if keywords_match:
                new_items.append(_item)

    return new_items


pantip_data = []


def get_data(keywords):
    pantip_data = []
    with yaspin(text='scraping..........'):
        while True:
            data = pantip_extract(keywords)
            pantip_data.extend(data)

            data_clean = []
            for i in range(len(pantip_data)):
                if pantip_data[i] not in pantip_data[i + 1:]:
                    data_clean.append(pantip_data[i])

            data_frame = pd.DataFrame(
                data_clean, columns=['title', 'description', 'link', 'published'])
            print("data length : ", len(data_frame))
            path = os.getcwd()
            data_frame.to_csv(path + '/export_dataframe.csv', header=True)
            time.sleep(180)


# get_data()
def main():
    search = input('input your keywords : ')
    clean = search.split(' ')
    print(clean)
    if len(clean) == 0:
        words = ''
    else:
        words = clean
    get_data(words)


main()
