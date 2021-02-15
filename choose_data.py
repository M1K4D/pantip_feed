import pandas as pd
import os

path = os.getcwd()
data_frame = pd.read_csv(path + '/raw_dataframe.csv')
data_list = data_frame.to_dict('records')
print(data_list)
# keyword = 'เพลง'
# data = []
# for data in data_list:
#     if data[1].find(keyword) != -1:
#         print(data)
