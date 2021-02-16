import pandas as pd
import os
import requests
import pandas as pd
path = os.getcwd()

url = "https://api.aiforthai.in.th/ssense"
path = os.getcwd()
data_frame = pd.read_csv(path + '/raw_dataframe.csv')
data_list = data_frame.to_dict('records')

choose = []
for data in data_list:
    text = str(data['description'])
    if text.find('หุ้น') != -1:
        choose.append(data)
results = []
for sen_ in choose:
    result = {}
    text = sen_['description']
    data = {'text': text}
    headers = {
        'Apikey': "NHSK9EnQDZNi5Rb24YKESf2BknHK6Ni0"
    }
    response = requests.post(url, data=data, headers=headers)
    sentiment = response.json()
    result['text'] = text
    result['sentiment'] = sentiment['sentiment']['polarity']
    results.append(result)

data_frame = pd.DataFrame(results, columns=['text', 'sentiment'])
data_frame.to_csv(path + '/sentimental.csv', header=True)
print(data_frame)
