import numpy as np
import pandas as pd
import glob
import datetime

# last_data = []
# for i in range(6):
#     data_path = glob.glob('./crawling_data/data_{}*'.format(i))[-1]
#     last_data.append(data_path)
# print(last_data)

data_path = glob.glob("./crawling_data/*")
print(data_path)

df = pd.DataFrame()
for path in data_path:
    df_temp = pd.read_csv(path, index_col=0)
    df = pd.concat([df, df_temp], axis = "rows", ignore_index = True)
df = df.replace('NULL', np.nan)
df = df.dropna()

print(df.head())
print(df["category"].value_counts())
print(df.info())
df.to_csv("./movie_concat_data_{}.csv".format(datetime.datetime.now().strftime("%Y%m%d")), index = False)