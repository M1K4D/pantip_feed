from typing import Text
from bs4 import BeautifulSoup
import requests
import feedparser
import pandas as pd
import time
import os
from yaspin import yaspin
path = os.getcwd()


def pantip_extract(keywords='', rawdata=[]):
    print(keywords)
    feed = feedparser.parse('https://pantip.com/forum/feed')
    new_items = []
    links = []
    for link in rawdata:
        links.append(link['link'])
    if len(keywords) == 0:
        for item in feed.entries:
            _item = {}

            _item['title'] = item.title
            _item['description'] = item.summary
            _item['link'] = item.link
            _item['published'] = item.published
            if item.link not in links:
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

            if keywords_match and item.link not in links:
                new_items.append(_item)

    return new_items


def get_data(keywords=''):
    try:
        data_frame = pd.read_csv(
            path + '/raw_dataframe.csv')
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
            data = pantip_extract(keywords=keywords, rawdata=data_list)
            data_list.extend(data)

            links = []
            for link in data_list:
                links.append(link['link'])

            remove_dup = []
            for i in range(len(data_list)):
                if data_list[i]['link'] not in links[i + 1:]:
                    remove_dup.append(data_list[i])

            data_frame = pd.DataFrame(
                data_list, columns=['title', 'description', 'link', 'published'])
            print("data length : ", len(data_list))

            data_frame.to_csv(
                '/home/m1k4/project/nodejs_search/raw_dataframe.csv', header=True)
            data_frame.to_csv(
                path + '/raw_dataframe.csv', header=True)
            time.sleep(200)


get_data(['การ์ตูน', 'อนิเมะ', 'เพลง', 'หุ้น', 'มังงะ'])
