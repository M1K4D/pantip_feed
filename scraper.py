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
path = os.getcwd()


def pantip_extract(keywords=''):
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

            new_items.append(_item)

    return new_items


def get_data(keywords=''):
    # print(keywords)
    try:
        data_frame = pd.read_csv(path + '/raw_dataframe.csv')
        data = data_frame.to_dict('records')
        data_list = []
        for list in data:
            item = {}
            item['title'] = list['title']
            item['description'] = list['description']
            item['link'] = list['link']
            item['published'] = list['published']
            data_list.append(item)
    except:
        data_list = []
    with yaspin(text='scraping..........'):
        while True:
            data = pantip_extract(keywords)
            data_list.extend(data)

            remove_dup = [i for n, i in enumerate(
                data_list) if i not in data_list[n + 1:]]

            data_frame = pd.DataFrame(
                remove_dup, columns=['title', 'description', 'link', 'published'])
            print("data length : ", len(remove_dup))

            data_frame.to_csv(path + '/raw_dataframe.csv', header=True)
            time.sleep(60)


get_data(['อนิเมะ'])
