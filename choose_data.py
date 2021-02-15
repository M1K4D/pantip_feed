import pandas as pd
import os

path = os.getcwd()
data_frame = pd.read_csv(path + '/export_dataframe.csv')
data_list = data_frame.values.tolist()
keyword = 'กินยา'
data = []
for data in data_list:
    if data[1].find(keyword) != -1:
        print(data)
