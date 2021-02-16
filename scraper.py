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
import ast
path = os.getcwd()


def pantip_extract(keywords=''):
    print(keywords)
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
                title = str(item.title)
                description = str(item.summary)
                find = title.find(keyword)
                des = description.find(keyword)

                if find >= 0 or des >= 0:
                    keywords_match = True

            if keywords_match:
                new_items.append(_item)

    return new_items


def get_data(keywords=''):
    try:
        data_frame = pd.read_csv(
            '/home/m1k4/project/nodejs_search/raw_dataframe2.csv')
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

            remove_dup = []
            for i in range(len(data_list)):
                if data_list[i] not in data_list[i + 1:]:
                    remove_dup.append(data_list[i])

            data_frame = pd.DataFrame(
                remove_dup, columns=['title', 'description', 'link', 'published'])
            print("data length : ", len(remove_dup))

            data_frame.to_csv(
                '/home/m1k4/project/nodejs_search/raw_dataframe2.csv', header=True)
            data_frame.to_csv(
                path + '/raw_dataframe2.csv', header=True)
            time.sleep(60)


get_data(['การ์ตูน', 'อนิเมะ', 'เพลง', 'หุ้น'])
