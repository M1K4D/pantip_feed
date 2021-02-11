import requests
from bs4 import BeautifulSoup
url = 'https://pantip.com/topic/40513315'

raw_data = requests.get(url)
raw_data.encoding = raw_data.apparent_encoding
print(raw_data.encoding)
print(raw_data.text)
